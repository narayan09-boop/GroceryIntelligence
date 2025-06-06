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
            
            # Try multiple OCR configurations for better results
            configs = [
                # Standard configuration with expanded character set
                r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,- $@/%&\'',
                # Alternative configuration for better line detection
                r'--oem 3 --psm 4',
                # Fallback configuration
                r'--oem 3 --psm 8'
            ]
            
            best_text = ""
            max_lines = 0
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed_image, config=config)
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    if len(lines) > max_lines:
                        max_lines = len(lines)
                        best_text = text
                except:
                    continue
            
            return best_text.strip() if best_text else ""
            
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def parse_items_and_prices(self, text):
        """Parse grocery items and prices from extracted text"""
        items = []
        lines = text.strip().split('\n')
        
        # More flexible grocery item patterns
        item_patterns = [
            # Pattern for items with prices like "ITEM NAME 12.99" or "ITEM NAME  12.99"
            r'^([A-Za-z][A-Za-z0-9\s\-\&\'\.\,\/\%]{1,40})\s+(\d{1,3}\.\d{2})$',
            # Pattern for items with prices like "ITEM NAME $12.99"
            r'^([A-Za-z][A-Za-z0-9\s\-\&\'\.\,\/\%]{1,40})\s+\$(\d{1,3}\.\d{2})$',
            # Pattern for quantity and items like "2 APPLES 5.99" or "1@ ITEM 3.99"
            r'^\d+[@\s]+([A-Za-z][A-Za-z0-9\s\-\&\'\.\,\/\%]{1,40})\s+(\d{1,3}\.\d{2})$',
            # Pattern for items with space and price "ITEM  5.99"
            r'^([A-Za-z][A-Za-z0-9\s\-\&\'\.\,\/\%]{1,40})\s{2,}(\d{1,3}\.\d{2})$',
            # Pattern for items on separate lines from prices
            r'^([A-Za-z][A-Za-z0-9\s\-\&\'\.\,\/\%]{1,40})$'
        ]
        
        # More flexible price patterns
        price_patterns = [
            r'^\$?(\d{1,3}\.\d{2})$',
            r'^(\d{1,3}\.\d{2})$',
            r'^\$(\d{1,3}\.\d{2})\s*$'
        ]
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line or len(line) < 3:
                i += 1
                continue
            
            # Skip common receipt headers/footers and non-item lines
            skip_patterns = [
                r'RECEIPT', r'TOTAL', r'SUBTOTAL', r'TAX', r'CHANGE', r'CASH',
                r'CREDIT', r'DEBIT', r'THANK YOU', r'STORE', r'DATE', r'TIME',
                r'CASHIER', r'REG#', r'TRANS#', r'BALANCE', r'TENDER', r'VISA',
                r'MASTERCARD', r'AMEX', r'DISCOVER', r'CARD', r'APPROVED',
                r'WELCOME', r'SAVE', r'COUPON', r'DISCOUNT', r'MEMBER',
                r'REWARDS', r'POINTS', r'PHONE', r'ADDRESS', r'STREET',
                r'CITY', r'STATE', r'ZIP', r'^\d{1,2}\/\d{1,2}\/\d{2,4}$',  # dates
                r'^\d{1,2}:\d{2}$',  # times
                r'^[A-Z]{2,}\s+\d+$',  # store codes
                r'^\*+$', r'^-+$', r'^=+$'  # separators
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
                        
                        # Clean item name and validate
                        item_name_clean = self.clean_item_name(item_name)
                        
                        # Validate price range and item name
                        if (0.01 <= price <= 999.99 and 
                            len(item_name_clean) >= 2 and
                            not re.match(r'^\d+$', item_name_clean) and  # not just numbers
                            not re.match(r'^[^A-Za-z]*$', item_name_clean)):  # contains letters
                            items.append({
                                'item': item_name_clean,
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
        
        # If no items found, try a more aggressive parsing approach
        if not items:
            items = self.fallback_parsing(lines)
        
        # Filter out duplicate items and clean up
        seen_items = set()
        unique_items = []
        
        for item in items:
            item_key = (item['item'].lower(), item['price'])
            if item_key not in seen_items:
                seen_items.add(item_key)
                unique_items.append(item)
        
        return unique_items
    
    def fallback_parsing(self, lines):
        """Fallback method for parsing when standard patterns fail"""
        items = []
        
        # Look for any line with text followed by a price-like number
        for line in lines:
            line = line.strip()
            if len(line) < 3:
                continue
                
            # Very broad pattern to catch price at end of line
            match = re.search(r'([A-Za-z][A-Za-z0-9\s\-\&\'\.\,\/\%]+?)\s+(\d{1,3}\.\d{2})\s*$', line)
            if match:
                item_name = self.clean_item_name(match.group(1))
                try:
                    price = float(match.group(2))
                    if (0.01 <= price <= 999.99 and 
                        len(item_name) >= 2 and
                        not re.match(r'^\d+$', item_name)):
                        items.append({
                            'item': item_name,
                            'price': price
                        })
                except ValueError:
                    continue
        
        return items
    
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
