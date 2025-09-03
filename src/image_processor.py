import os
from PIL import Image, ExifTags
from typing import Dict, List, Optional, Tuple
import logging

class ImageProcessor:
    """Handles image loading, processing, and metadata extraction"""
    
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif'}
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def is_supported_format(self, file_path: str) -> bool:
        """Check if file format is supported"""
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.SUPPORTED_FORMATS
    
    def load_image(self, file_path: str) -> Optional[Image.Image]:
        """Load an image from file path"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return None
            
            if not self.is_supported_format(file_path):
                self.logger.error(f"Unsupported format: {file_path}")
                return None
            
            return Image.open(file_path)
        except Exception as e:
            self.logger.error(f"Error loading image {file_path}: {e}")
            return None
    
    def extract_metadata(self, image: Image.Image, file_path: str) -> Dict:
        """Extract comprehensive metadata from image"""
        metadata = {
            'basic': {},
            'advanced': {},
            'exif': {},
            'file_info': {}
        }
        
        try:
            # Basic image information
            metadata['basic'] = {
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'width': image.width,
                'height': image.height,
                'bands': len(image.getbands()) if hasattr(image, 'getbands') else 'N/A'
            }
            
            # Advanced image parameters
            metadata['advanced'] = {
                'color_space': self._get_color_space(image.mode),
                'bits_per_pixel': self._get_bits_per_pixel(image),
                'has_alpha': 'Alpha' in image.mode,
                'is_animated': getattr(image, 'is_animated', False),
                'n_frames': getattr(image, 'n_frames', 1),
                'dpi': self._get_dpi_info(image),
                'compression': self._get_compression_info(image, file_path),
                'icc_profile': 'Yes' if hasattr(image, 'info') and 'icc_profile' in image.info else 'No'
            }
            
            # EXIF data if available
            if hasattr(image, '_getexif') and image._getexif():
                exif_data = image._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                        metadata['exif'][tag_name] = value
            
            # File information
            file_stats = os.stat(file_path)
            metadata['file_info'] = {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'file_size': file_stats.st_size,
                'file_size_mb': round(file_stats.st_size / (1024 * 1024), 2),
                'creation_time': file_stats.st_ctime,
                'modification_time': file_stats.st_mtime,
                'access_time': file_stats.st_atime
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting metadata: {e}")
        
        return metadata
    
    def _get_color_space(self, mode: str) -> str:
        """Get human-readable color space from image mode"""
        color_spaces = {
            '1': '1-bit Monochrome',
            'L': '8-bit Grayscale',
            'P': '8-bit Palette',
            'RGB': '24-bit RGB',
            'RGBA': '32-bit RGBA',
            'CMYK': '32-bit CMYK',
            'YCbCr': 'YCbCr',
            'LAB': 'LAB',
            'HSV': 'HSV'
        }
        return color_spaces.get(mode, mode)
    
    def _get_bits_per_pixel(self, image: Image.Image) -> int:
        """Calculate bits per pixel based on image mode and bands"""
        try:
            if hasattr(image, 'getbands'):
                bands = image.getbands()
                bits_per_band = 8  # Assuming 8 bits per channel for most formats
                return len(bands) * bits_per_band
            return 0
        except:
            return 0
    
    def _get_dpi_info(self, image: Image.Image) -> str:
        """Get DPI/PPI information if available"""
        try:
            dpi = image.info.get('dpi', (72, 72))
            if isinstance(dpi, tuple) and len(dpi) == 2:
                return f"{dpi[0]} x {dpi[1]} DPI"
            return str(dpi)
        except:
            return 'Unknown'
    
    def _get_compression_info(self, image: Image.Image, file_path: str) -> str:
        """Get compression information if available"""
        try:
            compression = image.info.get('compression', 'Unknown')
            if compression == 'jpeg':
                quality = image.info.get('quality', 'Unknown')
                return f"JPEG (Quality: {quality})"
            return str(compression).capitalize()
        except:
            return 'Unknown'
    
    def generate_thumbnail(self, image: Image.Image, size: Tuple[int, int] = (200, 200)) -> Image.Image:
        """Generate a thumbnail from the image"""
        try:
            thumbnail = image.copy()
            thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
            return thumbnail
        except Exception as e:
            self.logger.error(f"Error generating thumbnail: {e}")
            return image
    
    def get_folder_images(self, folder_path: str) -> List[str]:
        """Get all supported images from a folder"""
        if not os.path.isdir(folder_path):
            self.logger.error(f"Invalid folder path: {folder_path}")
            return []
        
        try:
            images = []
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and self.is_supported_format(file_path):
                    images.append(file_path)
            return images
        except Exception as e:
            self.logger.error(f"Error scanning folder {folder_path}: {e}")
            return []
