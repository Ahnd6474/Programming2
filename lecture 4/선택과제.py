from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional

Vector3 = List[float]
R = 8.314462618  # J/(mol·K), ideal gas constant


# ---------------------------
# Physics / Matter hierarchy
# ---------------------------

@dataclass
class Substance:
    """
    물질 기본 클래스 (Base class for matter).

    Attributes
    ----------
    name : str
        물질명.
    temperature : float
        절대온도 [K].
    """
    name: str
    temperature: float

    def set_temperature(self, T: float) -> None:
        """온도를 K 단위로 설정."""
        if T <= 0:
            raise ValueError("Temperature must be in Kelvin (>0).")
        self.temperature = T


@dataclass
class Fluid(Substance):
    """
    유체(액체/기체 공통) 클래스.

    Attributes
    ----------
    density : float
        밀도 [kg/m^3]. (기체는 상태에 따라 변할 수 있음)
    volume : float
        체적 [m^3].
    dynamic : bool
        시간/상태에 따라 변하는지 여부(모델링 편의 플래그).
    """
    density: float
    volume: float
    dynamic: bool = True

    def mass(self) -> float:
        """질량 [kg] = density * volume (단순 모델)."""
        return self.density * self.volume


class Gas(Fluid):
    """
    기체(이상기체) 클래스. Fluid를 상속.

    Attributes
    ----------
    pressure : float
        압력 [Pa].
    moles : float
        몰수 [mol].
    temperature : float
        절대온도 [K].

    Notes
    -----
    이상기체 근사: P·V = n·R·T
    - 상태 변경 시 미지수 1개를 이상기체식으로 계산합니다.
    - 단위: 압력 Pa, 체적 m^3, 온도 K, 기체상수 R=8.314...
    """

    def __init__(self, name: str, pressure: float, volume: float, moles: float, temperature: float):
        super().__init__(name=name, density=0.0, volume=volume, temperature=temperature, dynamic=True)
        if pressure <= 0 or volume <= 0 or moles <= 0 or temperature <= 0:
            raise ValueError("pressure, volume, moles, temperature must be > 0.")
        self.pressure = pressure
        self.moles = moles
        self._sync_density()

    # ---------- helpers ----------
    def _sync_density(self) -> None:
        """이상기체에서 질량 대신 밀도를 편의적으로 저장: ρ = (n·M)/V 가 맞지만
        몰질량 M을 모르면 ρ를 상태함수로 쓸 수 없음. 여기서는 단순화하여
        '상대적' 밀도 지표로 n/V 를 기록한다. (정확한 질량이 필요하면 M을 추가하세요.)
        """
        self.density = self.moles / self.volume  # mol/m^3 (단위상 진짜 질량밀도는 아님)

    def enforce_ideal_gas(self) -> None:
        """현재 P,V,n,T가 이상기체식을 만족하는지 검사(정보용). 불일치면 ValueError."""
        lhs = self.pressure * self.volume
        rhs = self.moles * R * self.temperature
        if abs(lhs - rhs) > max(1e-9, 1e-9 * rhs):
            raise ValueError("State does not satisfy ideal gas law (P·V != n·R·T).")

    # ---------- state setters ----------
    def set_state(self,
                  pressure: Optional[float] = None,
                  volume: Optional[float] = None,
                  moles: Optional[float] = None,
                  temperature: Optional[float] = None) -> None:
        """
        상태를 갱신합니다. 전달된 값들 중 '정확히 하나'가 None이어야 하며,
        그 하나를 PV=nRT로 계산합니다.

        Parameters
        ----------
        pressure, volume, moles, temperature : Optional[float]
            설정할 상태 변수. 네 변수 중 하나만 None이어야 함.

        Examples
        --------
        set_state(volume=0.02, moles=1.0, temperature=350.0, pressure=None)  # P를 계산
        """
        P = self.pressure if pressure is None else pressure
        V = self.volume if volume is None else volume
        n = self.moles if moles is None else moles
        T = self.temperature if temperature is None else temperature

        unknowns = [pressure is None, volume is None, moles is None, temperature is None]
        if sum(unknowns) != 1:
            raise ValueError("Exactly one of (pressure, volume, moles, temperature) must be None.")

        if pressure is None:
            # P = nRT / V
            if V <= 0 or n <= 0 or T <= 0:
                raise ValueError("V, n, T must be > 0.")
            P = n * R * T / V
        elif volume is None:
            # V = nRT / P
            if P <= 0 or n <= 0 or T <= 0:
                raise ValueError("P, n, T must be > 0.")
            V = n * R * T / P
        elif moles is None:
            # n = P V / (R T)
            if P <= 0 or V <= 0 or T <= 0:
                raise ValueError("P, V, T must be > 0.")
            n = P * V / (R * T)
        elif temperature is None:
            # T = P V / (n R)
            if P <= 0 or V <= 0 or n <= 0:
                raise ValueError("P, V, n must be > 0.")
            T = P * V / (n * R)

        # commit
        self.pressure, self.volume, self.moles, self.temperature = P, V, n, T
        self._sync_density()

    # ---------- thermodynamic processes ----------
    def isobaric(self, *, new_temperature: Optional[float] = None, new_volume: Optional[float] = None) -> None:
        """
        등압 과정(P=const): V ∝ T.
        new_temperature 또는 new_volume 중 하나만 지정.

        V2 = V1 * (T2/T1),  T2 = T1 * (V2/V1)
        """
        if (new_temperature is None) == (new_volume is None):
            raise ValueError("Specify exactly one of new_temperature or new_volume.")
        P, V1, n, T1 = self.pressure, self.volume, self.moles, self.temperature
        if new_temperature is not None:
            T2 = new_temperature
            if T2 <= 0:
                raise ValueError("Temperature must be > 0 K.")
            V2 = V1 * (T2 / T1)
            self.set_state(pressure=P, volume=V2, moles=n, temperature=T2)
        else:
            V2 = new_volume
            if V2 <= 0:
                raise ValueError("Volume must be > 0.")
            T2 = T1 * (V2 / V1)
            self.set_state(pressure=P, volume=V2, moles=n, temperature=T2)

    def isothermal(self, *, new_volume: Optional[float] = None, new_pressure: Optional[float] = None) -> None:
        """
        등온 과정(T=const): P ∝ 1/V.
        """
        if (new_volume is None) == (new_pressure is None):
            raise ValueError("Specify exactly one of new_volume or new_pressure.")
        T, n = self.temperature, self.moles
        if new_volume is not None:
            V2 = new_volume
            if V2 <= 0:
                raise ValueError("Volume must be > 0.")
            P2 = n * R * T / V2
            self.set_state(pressure=P2, volume=V2, moles=n, temperature=T)
        else:
            P2 = new_pressure
            if P2 <= 0:
                raise ValueError("Pressure must be > 0.")
            V2 = n * R * T / P2
            self.set_state(pressure=P2, volume=V2, moles=n, temperature=T)

    def isochoric(self, *, new_temperature: Optional[float] = None, new_pressure: Optional[float] = None) -> None:
        """
        정적 과정(V=const): P ∝ T.
        """
        if (new_temperature is None) == (new_pressure is None):
            raise ValueError("Specify exactly one of new_temperature or new_pressure.")
        V, n = self.volume, self.moles
        if new_temperature is not None:
            T2 = new_temperature
            if T2 <= 0:
                raise ValueError("Temperature must be > 0 K.")
            P2 = n * R * T2 / V
            self.set_state(pressure=P2, volume=V, moles=n, temperature=T2)
        else:
            P2 = new_pressure
            if P2 <= 0:
                raise ValueError("Pressure must be > 0.")
            T2 = P2 * V / (n * R)
            self.set_state(pressure=P2, volume=V, moles=n, temperature=T2)

    # ---------- conveniences ----------
    @classmethod
    def from_atm(cls, name: str, pressure_atm: float, volume_l: float, moles: float, temperature_c: float) -> "Gas":
        """
        편의 생성자: atm, L, °C 단위를 SI로 변환하여 Gas 생성.
        """
        P = pressure_atm * 101325.0
        V = volume_l / 1000.0
        T = temperature_c + 273.15
        return cls(name=name, pressure=P, volume=V, moles=moles, temperature=T)

    def __str__(self) -> str:
        return (f"[Gas {self.name}] P={self.pressure:.3g} Pa, V={self.volume:.3g} m^3, "
                f"n={self.moles:.3g} mol, T={self.temperature:.3g} K (ρ~{self.density:.3g} mol/m^3)")


# ---------------------------
# Rigid body dynamics
# ---------------------------

class PhysicalObject:
    """
    물리 객체 기본 클래스 (질점 모델).

    Attributes
    ----------
    name : str
        객체명.
    mass : float
        질량 [kg] (>0).
    position : list[float]
        [x, y, z] 위치 [m].
    velocity : list[float]
        [vx, vy, vz] 속도 [m/s].
    t : float
        누적 시간 [s].
    """

    def __init__(self,
                 name: str,
                 mass: float,
                 position: Optional[Vector3] = None,
                 velocity: Optional[Vector3] = None):
        if mass <= 0:
            raise ValueError("mass must be > 0.")
        self.name = name
        self.mass = mass
        self.position: Vector3 = list(position) if position is not None else [0.0, 0.0, 0.0]
        self.velocity: Vector3 = list(velocity) if velocity is not None else [0.0, 0.0, 0.0]
        self.t: float = 0.0
        self._force: Vector3 = [0.0, 0.0, 0.0]

    def apply_force(self, force: Vector3) -> None:
        """힘 누적 (N)."""
        self._force[0] += force[0]
        self._force[1] += force[1]
        self._force[2] += force[2]

    def clear_forces(self) -> None:
        """힘 누적 초기화."""
        self._force = [0.0, 0.0, 0.0]

    def update(self, dt: float, gravity: Optional[Vector3] = None) -> None:
        """
        시간 dt만큼 전진(세미-implicit Euler).

        Parameters
        ----------
        dt : float
            시간 간격 [s] (>0).
        gravity : Optional[Vector3]
            중력 가속도 [m/s^2]. 예: [0, -9.81, 0]
        """
        if dt <= 0:
            raise ValueError("dt must be > 0.")
        fx, fy, fz = self._force
        ax = fx / self.mass
        ay = fy / self.mass
        az = fz / self.mass
        if gravity is not None:
            ax += gravity[0]
            ay += gravity[1]
            az += gravity[2]

        # velocity update
        self.velocity[0] += ax * dt
        self.velocity[1] += ay * dt
        self.velocity[2] += az * dt

        # position update
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.position[2] += self.velocity[2] * dt

        self.t += dt
        self.clear_forces()

    def __str__(self) -> str:
        return f"[{self.name}] t={self.t:.3f}s pos={self.position} vel={self.velocity}"


class RigidBody(PhysicalObject):
    """
    강체(직육면체, 축 정렬) 모델.

    Attributes
    ----------
    size : list[float]
        [width, height, depth] [m].
    """

    def __init__(self,
                 name: str,
                 size: Tuple[float, float, float],
                 mass: float,
                 position: Optional[Vector3] = None,
                 velocity: Optional[Vector3] = None):
        super().__init__(name=name, mass=mass, position=position, velocity=velocity)
        if any(s <= 0 for s in size):
            raise ValueError("All size components must be > 0.")
        self.size = [float(size[0]), float(size[1]), float(size[2])]

    def get_corners(self) -> List[Tuple[float, float, float]]:
        """
        박스 8개 꼭짓점 좌표 반환 (축 정렬, 회전 없음).

        Returns
        -------
        list of (x,y,z)
        """
        cx, cy, cz = self.position
        w, h, d = self.size[0] / 2, self.size[1] / 2, self.size[2] / 2
        return [
            (cx - w, cy - h, cz - d),
            (cx + w, cy - h, cz - d),
            (cx + w, cy + h, cz - d),
            (cx - w, cy + h, cz - d),
            (cx - w, cy - h, cz + d),
            (cx + w, cy - h, cz + d),
            (cx + w, cy + h, cz + d),
            (cx - w, cy + h, cz + d),
        ]


# ---------------------------
# Quick demo / sanity check
# ---------------------------
if __name__ == "__main__":
    # Rigid body demo
    rb = RigidBody(name="Box1", size=(2.0, 1.0, 1.0), mass=5.0, position=[0.0, 0.0, 0.0])
    rb.apply_force([10.0, 0.0, 0.0])  # 10N in +x
    rb.update(0.1, gravity=[0.0, -9.81, 0.0])
    print(rb)
    print("Corners:", rb.get_corners())

    # Gas demo (from SI)
    gas = Gas(name="Helium", pressure=101325.0, volume=0.01, moles=0.5, temperature=300.0)
    print(gas)
    gas.isobaric(new_temperature=330.0)
    print("Isobaric to 330K:", gas)

    # Gas convenience (from atm/L/°C)
    gas2 = Gas.from_atm("Neon", pressure_atm=2.0, volume_l=3.0, moles=1.0, temperature_c=27.0)
    print(gas2)
    gas2.isothermal(new_volume=0.004)  # 등온, 체적 감소 → 압력 증가
    print("Isothermal (smaller V):", gas2)
