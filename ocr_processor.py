import pytesseract
import re
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

class OCRProcessor:
    def __init__(self):
        # Configure tesseract if needed
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust path as needed
        pass
    
    def preprocess_image(self, image):
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return image
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return image
    
    def extract_text(self, image):
        """Extract text from image using OCR"""
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            
            # Configure OCR parameters
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,- $'
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def parse_items_and_prices(self, text):
        """Parse grocery items and prices from extracted text"""
        items = []
        lines = text.strip().split('\n')
        
        # Common grocery item patterns
        item_patterns = [
            # Pattern for items with prices like "ITEM NAME 12.99"
            r'^([A-Za-z][A-Za-z\s\-\&\']{2,30})\s+(\d+\.\d{2})$',
            # Pattern for items with prices like "ITEM NAME $12.99"
            r'^([A-Za-z][A-Za-z\s\-\&\']{2,30})\s+\$(\d+\.\d{2})$',
            # Pattern for quantity and items like "2 APPLES 5.99"
            r'^\d+\s+([A-Za-z][A-Za-z\s\-\&\']{2,30})\s+(\d+\.\d{2})$',
            # Pattern for items on separate lines from prices
            r'^([A-Za-z][A-Za-z\s\-\&\']{2,30})$'
        ]
        
        # Price patterns for standalone prices
        price_patterns = [
            r'^\$?(\d+\.\d{2})$',
            r'^(\d+\.\d{2})$'
        ]
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line or len(line) < 3:
                i += 1
                continue
            
            # Skip common receipt headers/footers
            skip_patterns = [
                r'RECEIPT', r'TOTAL', r'SUBTOTAL', r'TAX', r'CHANGE', r'CASH',
                r'CREDIT', r'DEBIT', r'THANK YOU', r'STORE', r'DATE', r'TIME',
                r'CASHIER', r'REG#', r'TRANS#', r'BALANCE', r'TENDER'
            ]
            
            if any(re.search(pattern, line.upper()) for pattern in skip_patterns):
                i += 1
                continue
            
            # Try to match item with price on same line
            matched = False
            for pattern in item_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    if len(match.groups()) == 2:
                        item_name = match.group(1).strip().title()
                        price = float(match.group(2))
                        
                        # Validate price range (reasonable grocery prices)
                        if 0.01 <= price <= 999.99:
                            items.append({
                                'item': item_name,
                                'price': price
                            })
                            matched = True
                            break
                    elif len(match.groups()) == 1:
                        # Item name only, look for price on next line
                        item_name = match.group(1).strip().title()
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            for price_pattern in price_patterns:
                                price_match = re.match(price_pattern, next_line)
                                if price_match:
                                    price = float(price_match.group(1))
                                    if 0.01 <= price <= 999.99:
                                        items.append({
                                            'item': item_name,
                                            'price': price
                                        })
                                        matched = True
                                        i += 1  # Skip the price line
                                        break
                        if matched:
                            break
            
            i += 1
        
        # Filter out duplicate items and clean up
        seen_items = set()
        unique_items = []
        
        for item in items:
            item_key = (item['item'].lower(), item['price'])
            if item_key not in seen_items:
                seen_items.add(item_key)
                unique_items.append(item)
        
        return unique_items
    
    def clean_item_name(self, item_name):
        """Clean and standardize item names"""
        # Remove extra whitespace
        item_name = re.sub(r'\s+', ' ', item_name.strip())
        
        # Remove common prefixes/suffixes that don't help identification
        item_name = re.sub(r'^(ORGANIC|ORG|FRESH|PREMIUM|SELECT)\s+', '', item_name, flags=re.IGNORECASE)
        
        # Standardize common abbreviations
        replacements = {
            r'\bLB\b': 'POUND',
            r'\bOZ\b': 'OUNCE',
            r'\bPKG\b': 'PACKAGE',
            r'\bCT\b': 'COUNT'
        }
        
        for pattern, replacement in replacements.items():
            item_name = re.sub(pattern, replacement, item_name, flags=re.IGNORECASE)
        
        return item_name.title()
