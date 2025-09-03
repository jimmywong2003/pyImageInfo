import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QFileDialog, QListWidget, QListWidgetItem, QLabel, QTextEdit, 
                             QPushButton, QScrollArea, QGridLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QIcon
from image_processor import ImageProcessor

class ImageInfoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_processor = ImageProcessor()
        self.current_image_path = None
        self.current_image = None
        self.image_files = []
        self.current_index = 0
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('pyImageInfo - Image Metadata Viewer')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for left and right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - file browser and thumbnails
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # File selection buttons
        file_buttons_layout = QHBoxLayout()
        self.open_file_btn = QPushButton('Open File')
        self.open_folder_btn = QPushButton('Open Folder')
        file_buttons_layout.addWidget(self.open_file_btn)
        file_buttons_layout.addWidget(self.open_folder_btn)
        
        # Thumbnail list
        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.thumbnail_list.setIconSize(QSize(100, 100))
        self.thumbnail_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.thumbnail_list.setSpacing(10)
        
        left_layout.addLayout(file_buttons_layout)
        left_layout.addWidget(self.thumbnail_list)
        
        # Right panel - image view and metadata
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        
        # Metadata display
        self.metadata_text = QTextEdit()
        self.metadata_text.setReadOnly(True)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton('Previous')
        self.next_btn = QPushButton('Next')
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        
        right_layout.addWidget(self.image_label, 2)
        right_layout.addWidget(self.metadata_text, 3)
        right_layout.addLayout(nav_layout)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        
        # Connect signals
        self.open_file_btn.clicked.connect(self.open_file)
        self.open_folder_btn.clicked.connect(self.open_folder)
        self.thumbnail_list.itemClicked.connect(self.on_thumbnail_clicked)
        self.prev_btn.clicked.connect(self.previous_image)
        self.next_btn.clicked.connect(self.next_image)
        
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open Image', '', 
            'Images (*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.gif)'
        )
        if file_path:
            self.load_image(file_path)
            self.image_files = [file_path]
            self.current_index = 0
            self.update_thumbnail_list()
            
    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.image_files = self.image_processor.get_folder_images(folder_path)
            if self.image_files:
                self.current_index = 0
                self.load_image(self.image_files[0])
                self.update_thumbnail_list()
                
    def update_thumbnail_list(self):
        self.thumbnail_list.clear()
        for file_path in self.image_files:
            # Generate thumbnail
            image = self.image_processor.load_image(file_path)
            if image:
                thumbnail = self.image_processor.generate_thumbnail(image, (100, 100))
                if thumbnail:
                    # Convert PIL image to QPixmap - handle different image modes
                    if thumbnail.mode == 'RGB':
                        thumbnail_qimage = QImage(thumbnail.tobytes(), thumbnail.width, thumbnail.height, thumbnail.width * 3, QImage.Format.Format_RGB888)
                    elif thumbnail.mode == 'RGBA':
                        thumbnail_qimage = QImage(thumbnail.tobytes(), thumbnail.width, thumbnail.height, thumbnail.width * 4, QImage.Format.Format_RGBA8888)
                    else:
                        # Convert to RGB if mode is not supported
                        thumbnail = thumbnail.convert('RGB')
                        thumbnail_qimage = QImage(thumbnail.tobytes(), thumbnail.width, thumbnail.height, thumbnail.width * 3, QImage.Format.Format_RGB888)
                    
                    pixmap = QPixmap.fromImage(thumbnail_qimage)
                    item = QListWidgetItem(os.path.basename(file_path))
                    item.setIcon(QIcon(pixmap))  # Convert QPixmap to QIcon
                    item.setData(Qt.ItemDataRole.UserRole, file_path)
                    self.thumbnail_list.addItem(item)
            
    def on_thumbnail_clicked(self, item):
        index = self.thumbnail_list.row(item)
        if 0 <= index < len(self.image_files):
            self.current_index = index
            self.load_image(self.image_files[index])
            
    def load_image(self, file_path):
        self.current_image_path = file_path
        self.current_image = self.image_processor.load_image(file_path)
        
        if self.current_image:
            try:
                # Display image
                qimage = QImage(file_path)
                if qimage.isNull():
                    # Fallback: use PIL to load and convert
                    from PIL.ImageQt import ImageQt
                    qimage = ImageQt(self.current_image)
                
                pixmap = QPixmap.fromImage(qimage)
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                
                # Display metadata
                metadata = self.image_processor.extract_metadata(self.current_image, file_path)
                self.display_metadata(metadata)
                
                # Update window title with current file
                self.setWindowTitle(f'pyImageInfo - {os.path.basename(file_path)}')
                
            except Exception as e:
                self.show_error(f"Error loading image: {str(e)}")
        else:
            self.show_error(f"Failed to load image: {file_path}")
            
    def show_error(self, message):
        """Show error message in metadata area"""
        self.metadata_text.setPlainText(f"❌ ERROR:\n{message}")
        self.image_label.clear()
        self.image_label.setText("Image failed to load")
            
    def display_metadata(self, metadata):
        text = "<h2>📷 IMAGE METADATA</h2>"
        
        # Basic information
        text += "<h3>📋 BASIC INFORMATION</h3>"
        text += "<table style='width:100%; border-collapse: collapse;'>"
        for key, value in metadata['basic'].items():
            text += f"<tr><td style='padding: 4px; border: 1px solid #ddd; font-weight: bold;'>{key}</td><td style='padding: 4px; border: 1px solid #ddd;'>{value}</td></tr>"
        text += "</table>"
        
        # Advanced image parameters
        text += "<h3>⚙️ ADVANCED PARAMETERS</h3>"
        text += "<table style='width:100%; border-collapse: collapse;'>"
        for key, value in metadata['advanced'].items():
            # Format boolean values
            if isinstance(value, bool):
                value = 'Yes' if value else 'No'
            text += f"<tr><td style='padding: 4px; border: 1px solid #ddd; font-weight: bold;'>{key}</td><td style='padding: 4px; border: 1px solid #ddd;'>{value}</td></tr>"
        text += "</table>"
        
        # File information
        text += "<h3>📁 FILE INFORMATION</h3>"
        text += "<table style='width:100%; border-collapse: collapse;'>"
        for key, value in metadata['file_info'].items():
            if key not in ['file_path']:  # Skip full path to keep it clean
                # Format file size nicely
                if key == 'file_size':
                    value = f"{value:,} bytes"
                elif key == 'file_size_mb':
                    value = f"{value} MB"
                # Format timestamps
                elif key in ['creation_time', 'modification_time', 'access_time']:
                    from datetime import datetime
                    value = datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
                text += f"<tr><td style='padding: 4px; border: 1px solid #ddd; font-weight: bold;'>{key}</td><td style='padding: 4px; border: 1px solid #ddd;'>{value}</td></tr>"
        text += "</table>"
        
        # EXIF data
        text += "<h3>📊 EXIF DATA</h3>"
        if metadata['exif']:
            text += "<table style='width:100%; border-collapse: collapse;'>"
            for key, value in metadata['exif'].items():
                # Format some common EXIF tags for better readability
                formatted_value = value
                if isinstance(value, tuple):
                    formatted_value = str(value)
                elif isinstance(value, bytes):
                    try:
                        formatted_value = value.decode('utf-8', errors='ignore')
                    except:
                        formatted_value = str(value)
                text += f"<tr><td style='padding: 4px; border: 1px solid #ddd; font-weight: bold;'>{key}</td><td style='padding: 4px; border: 1px solid #ddd;'>{formatted_value}</td></tr>"
            text += "</table>"
        else:
            text += "<p>No EXIF data available</p>"
            
        self.metadata_text.setHtml(text)
        
    def previous_image(self):
        if self.image_files and len(self.image_files) > 1:
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.load_image(self.image_files[self.current_index])
            
    def next_image(self):
        if self.image_files and len(self.image_files) > 1:
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.load_image(self.image_files[self.current_index])

def main():
    app = QApplication(sys.argv)
    window = ImageInfoGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
