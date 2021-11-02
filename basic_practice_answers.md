# Ответы к практикуму по базовым фишкам Питона
I. При выполнении условия список заполняется генератором, а при невыполнении — остаётся пустым:
```py
orbEffects = [i for i in abilities if i.type == 'effect'] if not get_bit(status, 4) else []
```
II. Можно пройтись по кортежу B и проверить, находится ли каждый элемент в списке A:
```py
A = (1,2,3)
B = (2,4,5)
for i in B:
    if i not in A:
        print('Ну всё, приехали')
        break

>>> Ну всё, приехали
```
Можно обернуть это в функцию, чтобы она возвращала True/False и уже её можно было встроить в какой-нибудь `if`:
```py
A = (1,2,3,4,5)
B = (2,4,5)

def contain(x,y):
    for i in y:
        if i not in x:
            return False
    return True
    
if contain(A, B):
    print('Не((')
>>> Не((
```
Обратите внимание, что внутри функции мы можем назвать переменные как угодно, главное — подать в неё в качестве аргументов нужные переменные.  
Но есть и продвинутое решение этой задачи. Разность множеств — это вот так:  
![image](https://user-images.githubusercontent.com/56085790/139842483-7bf0cbe1-bf27-4c73-9395-08f5a68bc85e.png)  
И если `A` содержит все элементы `B`, то множество `B-A` будет пустое:  
```py
A = (1,2,3)
B = (2,4,5)

def contain(x,y):
    return set(y) - set(x)
    
print(contain(A, B))
>>> {4, 5}
```  
  
III. Расстояние находится по теореме Пифагора:
```py
def getrange(a, b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
```
IV. Всё очень просто, если использовать нужные функции:
```py
def randomtime():
    t = random.randint(0, int(time.time()))
    return time.ctime(t)
    
print(randomtime())
>>> Sat Nov 21 13:39:54 1992
```
  
V. Давайте используем словарь, чтобы записать "Привет" на разных языках:
```py
hellos = {'ru': 'Привет', 'en': 'Hi', 'jp': 'こんにちは', 'es': 'Buenos dias'}

def multihello(name, language='ru'):
    return f'{hellos[language]}, {name}!'
    
print(multihello('Дима'))
>>> Привет, Дима!
```
