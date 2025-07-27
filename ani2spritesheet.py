import io,os,sys
import logging
from wand.image import Image
from wand.color import Color

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)

def analyzeANIFile(filePath):
    with open(filePath,'rb') as f:
        if f.read(4) != b'RIFF':
            return {"code":-1,"msg":"File is not a ANI File!"}
        logging.debug('文件头检查完成！')
        fileSize = int.from_bytes(f.read(4), byteorder='little', signed=False)
        # if os.path.getsize(filePath) != fileSize:
        #     return {"code":-2,"msg":"File is damaged!"}
        logging.debug('文件长度检查完成！')
        if f.read(4) != b'ACON':
            return {"code":-1,"msg":"File is not a ANI File!"}
        logging.debug('魔数检查完成！')
        frameRate = (1/60)*1000
        while(True):
            chunkName = f.read(4)
            if chunkName == b'LIST':
                break
            chunkSize = int.from_bytes(f.read(4), byteorder='little', signed=False)
            if chunkName.lower() == b'rate':
                logging.debug('发现自定义速率！')
                frameRate = frameRate * int.from_bytes(f.read(4), byteorder='little', signed=False)
                logging.warning('发现自定义速率！由于GIF限制，将取第一帧与第二帧的速率作为整体速率！')
                f.read(chunkSize - 4)
            else:
                logging.debug('发现自定义Chunk！')
                f.read(chunkSize)
        listChunkSize = int.from_bytes(f.read(4), byteorder='little', signed=False)
        if f.read(4) != b'fram':
            return {"code":-3,"msg":"File not a ANI File!(No Frames)"}
        logging.debug('frame头检查完成！')
        frameList = []
        nowSize = 4
        while(nowSize < listChunkSize):
            if f.read(4) != b'icon':
                return {"code":-4,"msg":"File not a ANI File!(Other Kind Frames)"}
            nowSize += 4
            subChunkSize = int.from_bytes(f.read(4), byteorder='little', signed=False)
            nowSize += 4
            frameList.append(f.read(subChunkSize))
            nowSize += subChunkSize
        return {"code":0,"msg":frameList,"frameRate":frameRate}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.fatal("Usage: python ani2spritesheet.py <inputFileOrDir> <outputFileOrDir,Option>")
    else:
        inputPath = sys.argv[1]
        outputPath = sys.argv[2] if len(sys.argv) > 2 else inputPath 

        if os.path.isdir(inputPath):
            if not os.path.exists(outputPath):
                os.makedirs(outputPath) 
            for filename in os.listdir(inputPath):
                logging.info(f'Processing {filename}…')
                if filename.lower().endswith('.ani'):
                    filePath = os.path.join(inputPath, filename)
                    res = analyzeANIFile(filePath)
                    
                    if res["code"] == 0:
                        logging.info(f'ANIfile {filename} analyse completed, return success！')

                        # Open first frame to get actual size
                        with Image(file=io.BytesIO(res["msg"][0]), format='cur') as first_img:
                            sprite_width = first_img.width
                            sprite_height = first_img.height

                        frame_count = len(res["msg"])
                        logging.info(f'Frame size: {sprite_width}x{sprite_height}, Frame count: {frame_count}')
                        canvas_height = sprite_height * frame_count
                        spritesheet = Image(width=sprite_width, height=canvas_height, background=Color("transparent"))

                        for index, frame_bytes in enumerate(res["msg"]):
                            with Image(file=io.BytesIO(frame_bytes), format='cur') as img:
                                with Image(image=img.sequence[0]) as frame_img:
                                    top = index * sprite_height
                                    spritesheet.composite(frame_img, left=0, top=top)

                        outputFilePath = f"{outputPath}/{filename.strip('.ani')}.png"
                        spritesheet.save(filename=outputFilePath)                    
                        logging.info(f'SpriteSheet saved to {outputFilePath}！')           
                    else:
                        logging.fatal(res["msg"])
        
        elif os.path.isfile(inputPath):
            logging.info(f'Processing {outputPath}…')
            res = analyzeANIFile(inputPath)
            
            if res["code"] == 0:
                logging.info(f'ANIfile {outputPath} analyse completed, return success！')
                with Image(file=io.BytesIO(res["msg"][0]), format='cur') as img:
                    logging.info(f'Frame size: {img.width}x{img.height}')
                    if os.path.isdir(outputPath):
                        outputFilePath = os.path.join(outputPath, f"{os.path.basename(inputPath).strip('.ani')}.png")
                    else:
                        outputFilePath = f"{outputPath.strip('.png')}.png"
                    img.save(filename=outputFilePath)
                    
                logging.info(f'SpriteSheet saved to {outputFilePath}！')   
            else:
                logging.fatal(res["msg"])
        
        else:
            logging.fatal("Invalid input path!")
