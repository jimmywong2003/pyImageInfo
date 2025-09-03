# pyImageInfo

A powerful Python GUI application built with PyQt6 for viewing detailed image metadata and properties. This tool provides comprehensive information about your images including EXIF data, file information, and advanced image parameters.

![pyImageInfo Screenshot](https://via.placeholder.com/800x500/007acc/ffffff?text=pyImageInfo+GUI+Application)

## ✨ Features

- **📊 Comprehensive Metadata**: Extract detailed information from images including:
  - Basic image properties (format, dimensions, color mode)
  - Advanced parameters (color space, bits per pixel, DPI, compression)
  - EXIF data (camera settings, GPS coordinates, timestamps)
  - File information (size, creation/modification times)

- **🎨 Modern GUI**: Clean, intuitive interface built with PyQt6
  - Thumbnail navigation for easy browsing
  - Split-panel layout for efficient workflow
  - Responsive design with smooth image scaling

- **📁 Batch Processing**: Open individual files or entire folders
  - Navigate through images with Previous/Next buttons
  - Thumbnail grid view for quick selection

- **🖼️ Multi-format Support**: Works with popular image formats:
  - PNG, JPEG/JPG, BMP, TIFF/TIF, GIF

- **🚀 Standalone Executable**: Can be built as a single .exe file for easy distribution

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/jimmywong2003/pyImageInfo.git
cd pyImageInfo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

### Using the Standalone Executable

Download the latest release from the [Releases page](https://github.com/jimmywong2003/pyImageInfo/releases) and run `pyImageInfo.exe`.

## 🚀 Usage

1. **Launch the Application**: Run `python src/main.py` or double-click the executable
2. **Open Images**: 
   - Click "Open File" to select a single image
   - Click "Open Folder" to browse all images in a directory
3. **Navigate**: Use the thumbnail list or Previous/Next buttons to browse images
4. **View Metadata**: All image information is displayed in the right panel

### Metadata Categories

- **📋 Basic Information**: Format, dimensions, color mode, bands
- **⚙️ Advanced Parameters**: Color space, bits per pixel, alpha channel, animation, DPI, compression
- **📁 File Information**: File size, creation/modification times, file path
- **📊 EXIF Data**: Camera settings, GPS coordinates, timestamps (when available)

## 🛠️ Building from Source

To create a standalone executable:

1. Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
python build.py
```

3. The executable will be created in the `dist/` folder as `pyImageInfo.exe`

### Build Options

The build script supports several PyInstaller options:
- `--windowed`: No console window (GUI only)
- `--onefile`: Single executable file
- Custom icon support (uncomment in build.py)

## 📋 Supported Formats

| Format | Extension       | Notes                           |
| ------ | --------------- | ------------------------------- |
| PNG    | `.png`          | Full support with alpha channel |
| JPEG   | `.jpg`, `.jpeg` | EXIF data support               |
| BMP    | `.bmp`          | Basic bitmap support            |
| TIFF   | `.tiff`, `.tif` | Multi-page support              |
| GIF    | `.gif`          | Animation support               |

## 🏗️ Project Structure

```
pyImageInfo/
├── src/
│   ├── main.py          # Main GUI application
│   └── image_processor.py # Image processing and metadata extraction
├── build.py            # PyInstaller build script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── assets/            # Resources (icons, etc.)
```

## 🔧 Dependencies

- **PyQt6** >= 6.9.0 - GUI framework
- **Pillow** >= 11.0.0 - Image processing library
- **PyInstaller** >= 6.0.0 - Executable bundling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Bug Reports

If you encounter any issues, please [open an issue](https://github.com/jimmywong2003/pyImageInfo/issues) on GitHub with:
- A description of the problem
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)

## 📞 Support

For questions and support, please:
1. Check the [Issues](https://github.com/jimmywong2003/pyImageInfo/issues) page
2. Search existing discussions
3. Open a new issue if your question hasn't been answered

---

**pyImageInfo** - Your comprehensive image metadata viewer! 📷✨
