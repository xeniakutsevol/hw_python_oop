from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.duration_minutes = duration * self.MIN_IN_HOUR
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Реализовать метод в производных классах.")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    RUN_SPEED_1 = 18
    RUN_SPEED_2 = 20

    def get_spent_calories(self) -> float:
        return (
            (self.RUN_SPEED_1 * self.get_mean_speed() - self.RUN_SPEED_2)
            * self.weight
            / self.M_IN_KM
            * self.duration_minutes
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SW_WEIGHT = 0.035
    SW_SQUARE = 2
    SW_SPEED = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            self.SW_WEIGHT * self.weight
            + (self.get_mean_speed() ** self.SW_SQUARE // self.height)
            * self.SW_SPEED
            * self.weight
        ) * self.duration_minutes


class Swimming(Training):
    """Тренировка: плавание."""

    SWIM_SPEED = 1.1
    SWIM_SQUARE = 2
    LEN_STEP = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWIM_SPEED)
            * self.SWIM_SQUARE * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_codes = {"RUN": Running, "WLK": SportsWalking, "SWM": Swimming}
    if workout_type in class_codes:
        return class_codes[workout_type](*data)
    else:
        raise ValueError('Неизвестный тип тренировки.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
