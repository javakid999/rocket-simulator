import json
import math
import pygame

class AssetManager:
    def __init__(self):
        self.assets = {}
        self.assetList = [['./src/Assets/Images/cheese.png',(50,50)], ['./src/Assets/Images/background.jpg',-1], ['./src/Assets/Images/title.png',(600,100)]]

    def loadAssets(self):
        for asset in self.assetList:
            image = self.loadAsset(asset[0], asset[1])
            self.assets[image[1]] = image[0]
            
    @staticmethod
    def loadAsset(path, size=-1):
        if path.find('atlas') != -1:
            strings = path.split('-')
            name = strings[1]
            return [AssetManager.loadAtlas(path, (int(strings[2]), int(strings[3][0:strings[3].find('.')]))), name]
        else:
            name = path[path.rindex('/')+1:path.rindex('.')]
            image = pygame.image.load(path)
            if size != -1:   
                return [pygame.transform.scale(image, size), name]
            return [image, name]

    @staticmethod
    def loadAtlas(path, dimensions, subsurface=-1):
        asset = []
        atlas = pygame.image.load(path)
        if subsurface != -1:
            atlas = atlas.subsurface(pygame.Rect(*subsurface))
        for i in range(int(atlas.get_width() / dimensions[0])):
            asset.append([])
            for j in range(int(atlas.get_height() / dimensions[1])):
                asset[i].append(atlas.subsurface(pygame.Rect(i * dimensions[0], j * dimensions[1], dimensions[0], dimensions[1])))
        return asset
    
    @staticmethod
    def loadSpritesheet(imagepath, sheetpath, subsurface=-1):
        sprites = {}
        spritesheet = pygame.image.load(imagepath)
        if subsurface != -1:
            spritesheet = spritesheet.subsurface(pygame.Rect(*subsurface))
        mapsheet = json.load(open(sheetpath))
        for image in mapsheet.items():
            sprites[image[0]] = spritesheet.subsurface(pygame.Rect(*image[1]['dimensions']))
        
        return sprites

    @staticmethod
    def generateSpritesheet(imagepath, names, subsurface=-1):
        sprites = {}
        spritesheet = pygame.image.load(imagepath)
        if subsurface != -1:
            spritesheet = spritesheet.subsurface(pygame.Rect(*subsurface))
        mapsheet = AssetManager.generateRects(spritesheet)
        for i in range(len(names)):
            sprites[names[i]] = spritesheet.subsurface(pygame.Rect(*mapsheet[i]))

        return sprites

    @staticmethod
    def generateRects(image, dimensions=-1):
        masks = pygame.mask.from_surface(image).get_bounding_rects()

        if dimensions != -1:
            for mask in masks:
                if mask.width != dimensions[0]:
                    diff = dimensions[0] - mask.width
                    mask.x -= int(diff/2)
                    mask.width += diff
                if mask.height != dimensions[1]:
                    diff = dimensions[1] - mask.height
                    mask.y -= int(diff/2)
                    mask.height += diff

        n = len(masks)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if masks[j].y > masks[j + 1].y:
                    masks[j], masks[j + 1] = masks[j + 1], masks[j]
        
        n = len(masks)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if masks[j].x > masks[j + 1].x and ((masks[j].y >= masks[j + 1].y and masks[j].y <= masks[j+1].height + masks[j + 1].y) or (masks[j].y + masks[j].height >= masks[j + 1].y and masks[j].y + masks[j].height <= masks[j+1].height + masks[j + 1].y)):
                    masks[j], masks[j + 1] = masks[j + 1], masks[j]
        return masks

    # this will save an image of a generated texture atlas from various other atlases or spritesheets
    # use atlaspaths and atlasdimensions to load atlases
    # use sheetpaths and sheetdimensions to load spritesheets
    @staticmethod
    def generateTextureAtlas(finalDimensions, cols, **paths):
        images = []
        items = [*paths.keys()]

        if items.count('atlaspaths') > 0 and items.count('atlasdimensions') > 0:
            if len(paths['atlaspaths']) != len(paths['atlasdimensions']): 
                return False
            for i in range(len(paths['atlaspaths'])):
                atlasImages = AssetManager.loadAtlas(paths['atlaspaths'][i], paths['atlasdimensions'][i])
                for row in atlasImages:
                    for img in row:
                        images.append(img)
        if items.count('sheetpaths') > 0:
            if len(paths['sheetpaths']) != len(paths['sheetdimensions']): 
                return False
            for i in range(len(paths['sheetpaths'])):
                spritesheet = pygame.image.load(paths['sheetpaths'][i])
                sheetImages = AssetManager.generateRects(spritesheet, paths['sheetdimensions'][i])
                for rect in sheetImages:
                    images.append(pygame.transform.scale(spritesheet.subsurface(rect), (finalDimensions[0], finalDimensions[1])))
            
        for image in images:
            pygame.transform.scale(image, finalDimensions)
        surface = pygame.Surface((cols * finalDimensions[0], math.ceil(len(images)/cols) * finalDimensions[1]))

        for i in range(len(images)):
            surface.blit(images[i], (finalDimensions[0]*(i%cols),finalDimensions[1]*int(i/cols)))
        surface.set_colorkey((0,0,0))
        pygame.image.save(surface, 'spritesheet.png')
        return True