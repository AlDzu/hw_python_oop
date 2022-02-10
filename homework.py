class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:

         return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    training_name: str = 'Training'
    
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.training_name,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    training_name: str = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration_minutes = self.duration * 60
        mean_speed = self.get_mean_speed()
        calories = ((coeff_calorie_1 * mean_speed - coeff_calorie_2)
                    * self.weight / self.M_IN_KM * duration_minutes)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    training_name: str = 'SportsWalking'
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

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


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    LEN_STEP: float = 1.38
    training_name: str = 'Swimming'

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
        main(training)
