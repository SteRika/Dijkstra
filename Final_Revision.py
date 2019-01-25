from collections import defaultdict, deque
#from RPi import GPIO
from time import sleep
#import serial
#ser = serial.Serial('/dev/ttyACM0',9600)

global distance
distance = 0

#Motor1A = 16
#Motor1B = 18
#Motor1E = 22
##Motor2A = 19
#Motor2B = 21
#Motor2E = 23
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)

#GPIO.setup(Motor1A,GPIO.OUT)
#GPIO.setup(Motor1B,GPIO.OUT)
#GPIO.setup(Motor1E,GPIO.OUT)
#GPIO.setup(Motor2A,GPIO.OUT)
#GPIO.setup(Motor2B,GPIO.OUT)
#GPIO.setup(Motor2E,GPIO.OUT)

class Graph(object):
    def __init__(self):
        self.nodes = set() #titik awal
        self.edges = defaultdict(list) #list = array
        self.distances = {} #bobot
        self.direction = {}

    def add_node(self, value):
        self.nodes.add(value) #menambahkan node

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node) #menghubungkan Array
        self.edges[to_node].append(from_node) # kebalikan yang diatas
        self.distances[(from_node, to_node)] = distance #menghitung distance

    def add_direction(self , from_node , to_node , direction): #Penentuan Arah
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.direction[(from_node, to_node)] = direction
        
    def get_distances(self, from_node , to_node): #Mendapatkan Hasil Jarak
        return self.distances[from_node, to_node]

    def get_direction(self, from_node , to_node): #Mendapatkan arah gerak
        return self.direction[from_node, to_node]
        
    
def dijkstra(graph, initial): #pemrosesan Dijkstra 
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None 
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def path(graph, origin, destination): #Pencarian Jarak
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return list(full_path)  #visited[destination] , "cm"

def go(graph , origin , destination):
    y = leng(graph , origin , destination)
    x = full(graph , origin , destination , 'LJ')
    z = direction(graph , origin , destination)
    i = 0
    #ser.write(bytes(str(y),'UTF-8'))
    print(bytes(str(y), 'UTF-8'))
    #ser.write(bytes(';','UTF-8'))
    print(bytes(';','UTF-8'))
    for jarak in x  :
        for arah in z:

        #ser.write(bytes(str(jarak),'UTF-8'))
            print(bytes(str(jarak),'UTF-8'))
        #ser.write(bytes(';','UTF-8'))
            print(bytes(';','UTF-8'))
        #ser.write(bytes((str(z[i]),'UTF-8'))
            print(bytes(str(z[i]),'UTF-8'))
        #ser.write(bytes(';','UTF-8'))
            print(bytes(';','UTF-8'))
            i = i +1
        
            
        
def leng(graph , origin , destination):
    p = full(graph, origin , destination, 'output')
    x = 0
    for output_path in p:
        x += len(output_path)
    #ser.write(bytes(str(x) , 'UTF-8'))
    #ser.write(bytes(';','UTF-8'))
    return  x
    

def dist_from(graph, origin, destination): #Mengeluarkan Jarak Tempuh
    return graph.get_distances(origin, destination)

def direct(graph , origin , destination): #Mengeluarkan arah gerak
        arah = graph.get_direction(origin, destination)
        return arah
    
def direction(graph , origin , destination):
    output = path(graph , origin , destination)
    arah = list()
    for index in range(len(output) - 1):
        arah.insert(index,direct(graph, output[index] , output[index+1]))
    return arah

def full(graph , origin , destination, p_type): # Full DIjkstra dengan jarak , dan path
    output_path = path(graph, origin , destination)
    jarak = list()
    for index in range(len(output_path) - 1):
        jarak.insert(index, dist_from(graph , output_path[index] , output_path[index+1]))
    jumlah_jarak = sum(jarak)

    
    if (p_type == 'output'):    
        return output_path
    elif (p_type == 'total'):
        return jumlah_jarak
    elif (p_type == 'jarak1'):
        return jarak[0] 
    elif (p_type == 'jarak2'):
        return jarak[1]
    elif (p_type == 'jarak3'):
        return jarak[2]
    elif (p_type == 'jarak4'):
        return jarak[3]
    elif (p_type == 'jarak5'):
        return jarak[4]
    elif (p_type == 'jarak6'):
        return jarak[5]
    elif (p_type == 'jarak7'):
        return jarak[6]
    elif (p_type == 'jarak8'):
        return jarak[7]
    elif (p_type == 'LJ'):
        return jarak
    
        
def start(graph , origin , destination): #FULL Pergerakan Robot
    csum = 0
    i = 0
    distance = 0
    lastdistance = 0
    while 1 :
            distance = sensor(csum)
            if distance is None:
                distance = lastdistance
                
            lastdistance = distance
            l = full(graph , origin , destination, 'LJ')
            print(distance)
            
            if(i >= len(l)):
                i = 0
                s()
                print("ARRIVED")
                break

            if(distance > l[i]):
                s()
                print("Searching for next route")
                while distance > l[i]:
                    ser.write(bytes('A','UTF-8'))
                    distance = sensor(csum)
                    if distance is None:
                        distance = lastdistance
                    print(distance)
                print("Sensor Ready")
                sleep(5)
                i = i + 1
                
            elif ( distance < l[i]):
                output = path(graph, origin , destination)
                x = direct(graph, output[i] , output[i+1])
                
                if ( x == 0):
                    f()

                elif ( x == 1):
                    r()
                    

                elif ( x == 2):
                    lk()

                else :
                    s()

def sensor(csum): #Serial Komunikasi Dengan Arduino
        read = ser.readline()
        ser.flushInput()
        dataLen = len(read)
        if (dataLen > 2):
            csum = int(read[0:1])
        if (dataLen == csum and dataLen > 2):
            
            distance = int(read[1:dataLen])
            return distance
        
def f(): #maju
    print("GOING FORWARD")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH) 
    
    
    
def lk(): #kanan
    print ("Now Right")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def r(): #kiri
    print ("Now Left")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

def s(): #stop
    print ("Now stop")
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

#Global Inisialisasi
if __name__ == '__main__':
    graph = Graph()

    for node in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','z','1','2','3','4','5','6','7','8','9']:
        graph.add_node(node)# menambahkan node pada map dan Dijkstra
                #untuk direction ( 0 = lurus , 1 = kanan , 2 = kiri)

    graph.add_edge('a', 'b', 40)
    graph.add_direction('a', 'b', 0)
    graph.add_edge('b', 'a', 40)
    graph.add_direction('b', 'a', 0)
    graph.add_edge('b', 'p', 10)
    graph.add_direction('b', 'p', 1)
    graph.add_edge('p', 'c', 10)
    graph.add_direction('p', 'c', 0)
    graph.add_edge('b', 'q', 10)
    graph.add_direction('b', 'q', 2)
    graph.add_edge('q', 'd', 10)
    graph.add_direction('q', 'd', 0)
    graph.add_edge('b', 'e', 30)
    graph.add_direction('b', 'e', 0)
    graph.add_edge('c', 'g', 70)
    graph.add_direction('c', 'g', 0)
    graph.add_edge('c', 'b', 35)
    graph.add_direction('c', 'b', 0)
    graph.add_edge('d', 'b', 35)
    graph.add_direction('d', 'b', 0)
    graph.add_edge('d', 'f', 60)
    graph.add_direction('d', 'f', 0)
    graph.add_edge('e', 'b', 30)
    graph.add_direction('e', 'b', 0)
    graph.add_edge('e', 'i', 50)
    graph.add_direction('e', 'i', 0)
    graph.add_edge('f', 'd', 60)
    graph.add_direction('f', 'd', 0)
    graph.add_edge('f', 'r', 10)
    graph.add_direction('f', 'r', 1)
    graph.add_edge('r', 'j', 80)
    graph.add_direction('r', 'j', 0)
    graph.add_edge('g', 's', 10)
    graph.add_direction('g', 's', 1)
    graph.add_edge('s', 'h', 80)
    graph.add_direction('s', 'h', 0)
    graph.add_edge('h', 'g', 80)
    graph.add_edge('h', 't', 10)
    graph.add_direction('h' ,'t', 2)
    graph.add_edge('t', 'i', 105)
    graph.add_direction('t', 'i', 0)
    graph.add_edge('h', '6', 10)
    graph.add_direction('h' ,'6', 2)
    graph.add_edge('6', 'k', 25)
    graph.add_direction('6' ,'k', 0)
    graph.add_edge('i', 'e', 50)
    graph.add_edge('i', 'u', 10)
    graph.add_direction('i' ,'u', 1)
    graph.add_edge('u', 'h', 105)
    graph.add_direction('u' ,'h', 0)
    graph.add_edge('i', 'v', 10)
    graph.add_direction('i' ,'v', 2)
    graph.add_edge('v', 'j', 95)
    graph.add_direction('v' ,'j', 0)
    graph.add_edge('j', 'f', 80)
    graph.add_edge('j', 'w', 10)
    graph.add_direction('j' ,'w', 1)
    graph.add_edge('w', 'i', 95)
    graph.add_direction('w' ,'i', 0)
    graph.add_edge('j', '5', 35)
    graph.add_direction('j' ,'5', 1)
    graph.add_edge('5', 'o', 55)
    graph.add_direction('5' ,'o', 0)
    graph.add_edge('k', 'h', 25)
    graph.add_edge('k', 'y', 10)
    graph.add_direction('k' ,'y', 2)
    graph.add_edge('y', 'l', 105)
    graph.add_direction('y' , 'l', 0)
    graph.add_edge('k', 'm', 30)
    graph.add_direction('k' , 'm', 0)
    graph.add_edge('l', 'k', 105)
    graph.add_edge('l', 'z', 10)
    graph.add_direction('l' , 'z', 1)
    graph.add_edge('z', 'n', 30)
    graph.add_direction('z' , 'n', 0)
    graph.add_edge('m', 'k', 30)
    graph.add_edge('m', '1', 10)
    graph.add_direction('m' , '1', 2)
    graph.add_edge('1', 'n', 105)
    graph.add_direction('1' , 'n', 0)
    graph.add_edge('n', 'l', 30)
    graph.add_edge('n', '2', 10)
    graph.add_direction('n' , '2', 1)
    graph.add_edge('2', 'm', 105)
    graph.add_direction('2' , 'm', 0)
    graph.add_edge('n', '3', 10)
    graph.add_direction('n' ,'3' , 2)
    graph.add_edge('3', '0', 95)
    graph.add_direction('3' , '0', 0)
    graph.add_edge('o', 'j', 55)
    graph.add_edge('o', '4', 10)
    graph.add_direction('o' , '4', 1)
    graph.add_edge('4', 'n', 95)
    graph.add_direction('4' , 'n', 0)
    

    
    



