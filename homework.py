from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError('Калории считать в ' %
                                  (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_name: str = self.__class__.__name__
        return InfoMessage(training_name,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration_minutes = self.duration * 60
        mean_speed = self.get_mean_speed()
        calories = ((coeff_calorie_1 * mean_speed - coeff_calorie_2)
                    * self.weight / self.M_IN_KM * duration_minutes)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float = 1

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        duration_minutes = self.duration * 60
        mean_speed = self.get_mean_speed()
        calories = ((coeff_calorie_1 * self.weight + (mean_speed ** 2
                    // self.height) * coeff_calorie_2 * self.weight)
                    * duration_minutes)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float = 1
    count_pool: float = 1
    LEN_STEP: ClassVar[float] = 1.38

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""

        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""

        mean_speed = self.get_mean_speed()
        calories = (mean_speed + 1.1) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout = {'SWM': Swimming,
               'RUN': Running,
               'WLK': SportsWalking}
    if workout_type in workout:
        result = workout[workout_type](*data)
        return result
    else:
        return(f'Неизвестный вид тренировки')


def main(training: Training) -> None:
    """Главная функция."""

    info = InfoMessage.get_message(training.show_training_info())
    print(info)


training: Training = Training

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training == 'Неизвестный вид тренировки':
            print('Неизвестный вид тренировки')
        else:
            main(training)
