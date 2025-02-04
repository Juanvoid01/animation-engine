#scene_code.py

from scene.scene import Scene
from objects.code_string import CodeString

class SceneCode(Scene):
    """Scene"""

    def __init__(self):
        super().__init__()
        sample_code = """
#include <iostream>

using namespace std;
static const int akkkk = 0;
class pepe
{
public:
private: 
};
bool x;
enum {a,b,c};
typedef struct c
{
    int num = 14123;
} pepe;

struct goloo;
int asadad();
int main()
{
    int arr[] = {1,2};
    
    int asd = (2+3 ^2);
    uint16_t* a = (uint16_t*)&asd;
    a = new(uint16_t);
    delete a;
    pepe pepes;
    return 0;
    std::cout << "hola" << std::endl;
    for(int i = 0; i < 100; i++);
    while(true);
}
// pepe
        """
        self.code = CodeString(100, 50, 700, code_text=sample_code)
        self.code.highlight_line(24)

    def update(self, tick):
        self.code.update(tick)
    
    def draw(self, screen):
        self.code.draw(screen)

    def finish(self):
       return True