import math

class PerlinNoise:
    @staticmethod
    def generate_values(seed, depth, num):
        values = []
        for i in range(num):
            values.append(PerlinNoise.fbm([0,i/10], seed, 0.5, 1, depth))
        return values

    @staticmethod
    def sserp(a, b, x):
        return (b - a) * ((x * (x * 6 - 15) + 10) * x * x * x) + a
    
    @staticmethod
    def lerp(a, b, x):
        return (1-x) * a + x * b

    @staticmethod
    def random2d(uv, seed):
        return math.fmod(math.sin(uv[0] * 12.9898 + uv[1] * 78.233 + seed)*43758.5453123,1)
    
    @staticmethod
    def rotate(vec, r):
        return [vec[0] * math.cos(r) - vec[1] * math.sin(r), vec[0] * math.sin(r) + vec[1] * math.cos(r)]

    #this literally doesn't work, I have no idea why, and it is only functioning because of a hack (don't try to use negative uv coordinates!!!!)
    @staticmethod
    def perlinNoise(uv, seed):
        TL = [math.floor(uv[0]),math.floor(uv[1])]
        TR = [math.ceil(uv[0]),math.floor(uv[1])]
        BL = [math.floor(uv[0]),math.ceil(uv[1])]
        BR = [math.ceil(uv[0]),math.ceil(uv[1])]
        
        gradTL = [math.cos(PerlinNoise.random2d(TL, seed) * 6.283), math.sin(PerlinNoise.random2d(TL, seed) * 6.283)]
        toTL = [uv[0]  - TL[0], uv[1] - TL[1]]
        gradTR = [math.cos(PerlinNoise.random2d(TR, seed) * 6.283), math.sin(PerlinNoise.random2d(TR, seed) * 6.283)]
        toTR = [uv[0]  - TR[0], uv[1] - TR[1]]
        
        gradBL = [math.cos(PerlinNoise.random2d(BL, seed) * 6.283), math.sin(PerlinNoise.random2d(BL, seed) * 6.283)]
        toBL = [uv[0]  - BL[0], uv[1] - BL[1]]
        gradBR = [math.cos(PerlinNoise.random2d(BR, seed) * 6.283), math.sin(PerlinNoise.random2d(BR, seed) * 6.283)]
        toBR = [uv[0]  - BR[0], uv[1] - BR[1]]
        
        t = PerlinNoise.sserp(gradTL[0] * toTL[0] + gradTL[1] * toTL[1], gradTR[0] * toTR[0] + gradTR[1] * toTR[1], uv[0] % 1)
        b = PerlinNoise.sserp(gradBL[0] * toBL[0] + gradBL[1] * toBL[1], gradBR[0] * toBR[0] + gradBR[1] * toBR[1], uv[0] % 1)
        return PerlinNoise.sserp(t,b,uv[1] % 1) + 0.5
    
    @staticmethod
    def fbm(uv, seed, contribution, scale, octaves):
        sum = 0
        for n in range(octaves):
                    sum += PerlinNoise.perlinNoise([uv[0]*scale+scale,uv[1]*scale+scale], seed) * contribution
                    contribution *= 0.5
                    scale *= 2
                    uv = PerlinNoise.rotate(uv, 1.2)
        return min(max(sum,0),1)-0.5