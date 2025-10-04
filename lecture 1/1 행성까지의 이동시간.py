name = input("행성 이름: ")
distance = input("행성까지의 거리(km): ")
speed = input("이동 속도(km/h): ")

distance = int(distance)
speed = int(speed)

totalTime = distance//speed
year = int(totalTime/24//365)
month = int(totalTime/24%365//30)
day = totalTime//24%365%30
time = totalTime%24

print(f'지구-{name} 이동 시간: {totalTime}시간')
print(f'지구-{name} 이동 시간: {year}년 {month}월 {day}일 {time}시간')