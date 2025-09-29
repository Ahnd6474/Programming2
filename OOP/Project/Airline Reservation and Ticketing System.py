class Flight:
    """
    항공편 정보 클래스
    """

    def __init__(self, flight_number: str, origin: str, destination: str, total_seats: int, departure: str):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.total_seats = total_seats
        self.reserved_seats = 0
        self.departure = departure
        self.reservations = []

    def check_availability(self) -> int:
        """
        항공편의 이용 가능 좌석 수를 반환합니다.
        """
        return self.total_seats - self.reserved_seats


class Customer:
    """
    고객 정보 클래스
    """

    """
    [문제1] __init__과 __str__ 메소드를 작성하세요.
    - 지시 사항:
      1. Customer 클래스는 customer_id, name, email, 고객의 모든 예약 이력을 저장할 리스트
         reservation_history를 속성으로 가집니다. reservation_history는 빈 리스트로 초기화하세요.
      2. print, str 함수에서 Customer 객체의 정보를
         "👤 고객 ID: C001, 이름: 김민지, 이메일: kim@example.com"
         형식으로 사용할 수 있도록 메소드를 정의해주세요.
    """

    # TO DO ...


class Reservation:
    """
    고객의 항공편 예약을 나타내는 클래스
    """

    def __init__(self, reservation_id: str, customer: Customer, flight: Flight, seat_number: str):
        self.reservation_id = reservation_id
        self.customer = customer
        self.flight = flight
        self.seat_number = seat_number
        self.is_issued = False


class AirlineSystem:
    """
    항공편, 고객, 예약을 총괄하는 시스템
    """

    def __init__(self):
        self.flights = {}
        self.customers = {}
        self.next_reservation_id = 1

    def add_flight(self, flight: Flight) -> None:
        """
        [문제2] Flight 객체를 항공사 시스템에 추가하는 메서드를 완성하세요.
        - 지시 사항:
           입력받은 Flight 객체를 인스턴스 변수 flights 딕셔너리에 추가하세요.
           키는 항공편 번호(flight.flight_number)입니다.
        """
        # TO DO ...
        print(f"✈ 항공편 등록: {flight.flight_number}")

    def add_customer(self, customer: Customer) -> None:
        """
        [문제2] Customer 객체를 항공사 시스템에 추가하는 메서드를 완성하세요.
        - 지시 사항:
           입력받은 Customer 객체를 인스턴스 변수 customers 딕셔너리에 추가하세요.
           키는 고객 ID(customer.customer_id)입니다.
        """
        # TO DO ...
        print(f"👤 고객 등록: {customer.customer_id}")

    def make_reservation(self, customer_id: str, flight_number: str, seat_number: str) -> Reservation | None:
        """
        [문제3] 좌석을 예약하는 메서드를 완성하세요.
        - 지시 사항:
          1. customer_id가 self.customers에, flight_number가 self.flights에 존재하는지 확인하세요.
          2. 해당 항공편의 잔여 좌석이 있는지 확인하세요.
          3. 모든 조건이 충족되면 Reservation 객체를 생성하세요. 이때 reservation_id는
             self.next_reservation_id를 활용하여 고유하게 만드세요. “R”과 reservation_id를 4자리로 표현한 문자열
             형태이며, f-string을 활용하세요. (f"R{self.next_reservation_id:04d}")
          4. 생성된 Reservation 객체를 고객의 reservation_history 리스트와 항공편의 reservations 리스트에 각각
             추가하세요.
          5. 항공편의 reserved_seats를 1 증가시키고, self.next_reservation_id도 1 증가시키세요.
        """
        if customer_id not in self.customers:
            print(f"❌ 예약 실패: 고객 ID({customer_id})를 찾을 수 없음")
            return None

        # TO DO ...

    def find_reservation(self, reservation_id: str) -> Reservation | None:
        """
        [문제4] 예약 ID를 사용하여 예약 객체를 찾는 메서드를 완성하세요.
        - 지시 사항:
          1. 모든 고객 또는 모든 항공편의 예약 기록 리스트(Reservation 객체 리스트)에서 각 예약 객체의
             reservation_id가 메소드의 인자와 일치하는지 확인하세요.
          2. 일치하는 객체를 찾으면 해당 Reservation 객체를 반환하고, 메소드를 빠져나가세요.
          3. 만약 모든 고객의 기록을 확인해도 일치하는 예약을 찾지 못하면 None을 반환하세요.
        """
        # TO DO ...

    def issue_ticket(self, reservation_id: str) -> None:
        """
        [문제5] 항공권을 발권하는 메서드를 완성하세요.
        - 지시 사항:
          1. find_reservation()을 사용하여 주어진 reservation_id에 해당하는 예약 객체를 찾으세요.
          2. 해당 예약이 이미 발권되었는지 확인하세요.
          3. 유효한 예약이면 발권 상태(is_issued)를 True로 변경하세요.
        """
        # TO DO ...

    def cancel_reservation(self, reservation_id: str) -> None:
        """
        [문제6] 예약을 취소하는 메서드를 완성하세요.
        - 지시 사항:
          1. find_reservation 메서드를 사용하여 reservation_id에 해당하는 예약 객체를 찾으세요.
          2. 찾은 예약 객체의 해당 고객의 reservation_history 리스트와 항공편의 reservations 리스트에서 예약
             객체를 제거하세요.
          3. 항공편의 reserved_seats 수를 1 감소시키세요.
        """
        # TO DO ...


if __name__ == '__main__':
    system = AirlineSystem()

    # ✈ 항공편 및 👤 고객 등록
    # 전체 좌석수는 잔여 좌석 부족 상황을 시뮬레이션하기 위해 작게 설정함
    flight_oz = Flight("OZ764", "ICN", "JFK", 2, "2025-10-19 10:00")
    flight_ke = Flight("KE901", "ICN", "CDG", 1, "2025-10-19 10:00")
    customer_kim = Customer("C001", "김민지", "kim@example.com")
    customer_park = Customer("C002", "박서준", "park@example.com")

    system.add_flight(flight_oz)
    system.add_flight(flight_ke)
    system.add_customer(customer_kim)
    system.add_customer(customer_park)

    # --- 모든 고객 정보 확인 ---
    print("\n--- 전체 고객 ---")
    for customer in system.customers.values():
        print(f"👤 {customer}")

    # --- 시나리오 1: 정상적인 예약, 발권, 취소 ---
    print("\n--- 시나리오 1: 정상적인 예약, 발권, 취소 ---")
    res1 = system.make_reservation("C001", "OZ764", "10A")
    if res1:
        system.issue_ticket(res1.reservation_id)
        system.cancel_reservation(res1.reservation_id)

    print(f"\nOZ764 항공편 잔여 좌석: {flight_oz.check_availability()}개")

    # --- 시나리오 2: 예약 실패 (존재하지 않는 ID) ---
    print("\n--- 시나리오 2: 존재하지 않는 고객 또는 항공편으로 예약 시도 ---")
    system.make_reservation("C999", "OZ764", "10B")
    system.make_reservation("C001", "AA123", "10C")

    # --- 시나리오 3: 잔여 좌석 부족으로 예약 실패 ---
    print("\n--- 시나리오 3: 잔여 좌석 부족으로 예약 실패 ---")
    res2 = system.make_reservation("C001", "KE901", "20A")
    res3 = system.make_reservation("C002", "KE901", "20B")

    print(f"\nKE901 항공편 잔여 좌석: {flight_ke.check_availability()}개")

    # --- 시나리오 4: 발권 및 취소 실패 (유효하지 않은 예약 ID) ---
    print("\n--- 시나리오 4: 유효하지 않은 ID로 발권 및 취소 시도 ---")
    system.issue_ticket("R9999")
    system.cancel_reservation("R9999")

    # --- 시나리오 5: 중복 발권 및 재취소 시도 ---
    print("\n--- 시나리오 5: 중복 발권 및 재취소 시도 ---")
    if res2:
        system.issue_ticket(res2.reservation_id)
        system.issue_ticket(res2.reservation_id)

        system.cancel_reservation(res2.reservation_id)
        system.cancel_reservation(res2.reservation_id)
