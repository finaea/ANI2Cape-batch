# Fork

This fork made a few enhancements:
- Allow batch processing for converting ANI to SpriteSheet
- Resolve non-transparent spritesheet output
- Removed fixed Output Size
- Log frame size and count

# Requirements

This fork changed Pillow library to ImageMagick:
1. Install ImageMagick by following the guide https://docs.wand-py.org/en/latest/guide/install.html and setup env variable for `$MAGICK_HOME`.
2. Run `pip install Wand`


# ANI2Cape

A tool that can convert Windows Animated Cursors (*.ani) to GIF/Pillow Images/Cape format

- [x] ANI2Pillow Image
- [x] ANI2GIF(ANI2Pillow Image + Pillow Image2GIF)
- [x] GIF2SpriteSheet(GIF2Pillow Image + Pillow Image2SpriteSheet)
- [x] ANI2Cape

`Usage:python XXX.py <inputFile> <outputFile,Option>`

- [x] ANI2SpriteSheet(GIF2Pillow Image + Pillow Image2SpriteSheet)

`Usage:python XXX.py <inputFilOrDir> <outputFileOrDir,Option>`
