import torch 
import torch.nn as nn

class block(nn.Module):
    def __init__(self,in_channels,out_channels,stride=2):
        super().__init__()
        self.conv=nn.Sequential(
            nn.Conv2d(in_channels,out_channels,4,stride,1,bias=False,padding_mode="reflect"),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2),
        )
    
    def forward(self,x):
        return self.conv(x)
    

class Discriminator(nn.Module):
    def __init__(self,in_channels=3,features=[64,128,256,512]):
        super().__init__()
        self.inital=nn.Sequential(
            nn.Conv2d(in_channels*2,features[0],4,2,1,padding_mode="reflect"),
            nn.LeakyReLU(0.2),
        )
        
        layers=[]
        in_channels=features[0]
        for feature in features[1:]:
            layers.append(block(in_channels,feature,stride=1 if feature==features[-1] else 2))
            in_channels=feature
            
        layers.append(nn.Conv2d(in_channels,1,4,1,1,padding_mode="reflect"))
        self.model=nn.Sequential(*layers)
        
    def forward(self,x,y):
        x=torch.cat([x,y],dim=1)
        x=self.inital(x)
        return self.model(x)
    
def test():
    x=torch.randn((1,3,256,256))
    y=torch.randn((1,3,256,256))
    model=Discriminator(in_channels=3)
    preds=model(x,y)
    print(preds.shape)
    
