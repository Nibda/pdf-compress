import os

"Отримуємо файли (з повним шляхом) у поточній та вкладених директоріях"
# for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
# 	for file in files:
# 		if file.endswith(".pdf"):
# 			print(os.path.join(root, file))

"Назва файлу програми, яка зараз викнується"
print('__file__:', __file__, type(__file__))

"Повний шлях з назвою файлу"
abspath = os.path.abspath(__file__)
print('os.path.abspath:', abspath, type(abspath))

"Шлях без назви файлу"
dirname = os.path.dirname(__file__)
print('os.path.dirname:', dirname, type(dirname))

"Відокремлення назви файлу від шляху"
filename = os.path.basename(__file__)
print("os.path.basename:", filename)

"видає кортеж у якому першим елементом видається шлях, а другим назва файлу"
pathsplit = os.path.split(__file__)
print("os.path.split:", pathsplit)

"Видає кортеж де першим елементом виск, а другим усе решта з назвою файлу"
splitdrive = os.path.splitdrive(__file__)
print("os.path.splitdrive:", splitdrive)

"Видає кортеж, де першим елементом є шлях з назвою файлу, а другий - розширення"
splitext = os.path.splitext(__file__)
print("os.path.splitext:", splitext)

path = r"d:\python\PDF compress\ЕЙ СІ РЕНТ ГРУП\бондаренко андрій дмитрович\secrecy agreement.pdf"
join = os.path.join(*os.path.normpath(path).split(os.sep)[-2:])
print('join:', join)

"список файлів"
print("os.listdir():")
print(os.listdir())

"Склейка"
print(os.path.join(dirname, "copmress", filename))

# print(os.path.dirname(os.path.abspath(__file__)))

for root in os.walk(os.path.dirname(__file__)+r"\test"):
	print(root)

path = os.path.normpath(r"d:\python\PDF compress\test\OPTIMIZED\employment agreement.pdf")
# print(path)
# d = path.split(os.path.normpath(os.path.split(dirname)[0]))
# print(d)


for root, dirs, files in os.walk(os.path.dirname(__file__)):
	# print(root)
	for file in files:
		if file.endswith("autobiography_compressed.pdf"):
			p1 = os.path.join(root, file)
			break
print("-----", p1)





