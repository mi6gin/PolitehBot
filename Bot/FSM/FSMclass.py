from aiogram.fsm.state import StatesGroup, State


class FSM(StatesGroup):
    Start = State()
    Auth = State()
    End = State()
    Finish = State()
    Deauth = State()

    DistCour = State()
    DistCour_thcr = State()
    Schedule = State()
    Jornal = State()
    Examus = State()
    Umkd = State()
    Practics = State()
    Adviser = State()
    Transkript = State()
    Plan = State()
    Calendar = State()
    Userplan = State()

    Jornaltch = State()
    Attendance = State()
    Schld = State()
    SchldEX = State()
    Umkdtch = State()
    Praktika = State()
    Students = State()
