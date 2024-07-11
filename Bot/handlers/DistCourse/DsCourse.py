from aiogram import Dispatcher, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM.FSMclass import FSM
from handlers.AccountManager import Keyboard
from handlers.DistCourse import Get_schedule, Get_jornal, Get_umkd, Get_examus, Get_practics, Get_adviser, Get_transkript, Get_Plan, Get_academcalendar, Get_userplan, Get_jornal_tch, Get_attendance, Get_schld_tch, Get_shchldex, Get_umkd_tch, Get_practika, Get_students



async def dist_course(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await message.message.answer(
        text=f'Дистанционные курсы',
        reply_markup= await Keyboard.get_keyboard_distant(message, user_id)
    )
    await state.update_data(message_to_delete=message_to_delete)

async def dist_course_for_tchr(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await message.message.answer(
        text=f'Дистанционные курсы',
        reply_markup= await Keyboard.get_keyboard_distant_thcr(message, user_id)
    )
    await state.update_data(message_to_delete=message_to_delete)

def register_handlers_cComm(nihao: Dispatcher):
    nihao.callback_query.register(dist_course, lambda c: c.data == 'dscourse')
    nihao.callback_query.register(dist_course_for_tchr, lambda c: c.data == 'dscourse_tch')
    nihao.callback_query.register(Get_schedule.schedule, lambda c: c.data == 'grafics')
    nihao.callback_query.register(Get_schedule.schedule_znml, lambda c: c.data == 'znml')
    nihao.callback_query.register(Get_schedule.schedule_chsl, lambda c: c.data == 'chsl')
    nihao.callback_query.register(Get_jornal.jornal, lambda c: c.data == 'jornal')
    nihao.callback_query.register(Get_umkd.umkd, lambda c: c.data == 'umkd')
    nihao.callback_query.register(Get_umkd.button_pressed_umkd, lambda c: c.data.startswith('umkd:'))
    nihao.callback_query.register(Get_umkd.button_pressed_umkd_num2, lambda c: c.data.startswith('umkdp:'))
    nihao.callback_query.register(Get_umkd.button_pressed_umkd_download, lambda c: c.data.startswith('umkds:'))
    nihao.callback_query.register(Get_examus.examus, lambda c: c.data =='examus')
    nihao.callback_query.register(Get_practics.practics, lambda c: c.data == 'pract')
    nihao.callback_query.register(Get_adviser.Adviser, lambda c: c.data == 'adviser')
    nihao.callback_query.register(Get_transkript.Transkript, lambda c: c.data == 'trans')
    nihao.callback_query.register(Get_Plan.plan, lambda c: c.data == 'plan')
    nihao.callback_query.register(Get_academcalendar.Calendar, lambda c: c.data == 'calendar')
    nihao.callback_query.register(Get_userplan.Userplan, lambda c: c.data == 'userplan')
    nihao.callback_query.register(Get_userplan.button_pressed_userplan_num2, lambda c: c.data.startswith('userplan:'))
    nihao.callback_query.register(Get_jornal_tch.jornal, lambda c: c.data == 'jornal_tch')
    nihao.callback_query.register(Get_attendance.jornal, lambda c: c.data == 'attest')
    nihao.callback_query.register(Get_schld_tch.schld, lambda c: c.data == 'shld')
    nihao.callback_query.register(Get_shchldex.schld, lambda c: c.data == 'shldex')
    nihao.callback_query.register(Get_practika.jornal, lambda c: c.data == 'practika')
    nihao.callback_query.register(Get_students.std, lambda c: c.data == 'spisok')

    nihao.callback_query.register(Get_umkd_tch.umkd, lambda c: c.data == 'umkd_tch')
    nihao.callback_query.register(Get_umkd_tch.button_pressed_umkd, lambda c: c.data.startswith('umkd1:'))
    nihao.callback_query.register(Get_umkd_tch.button_pressed_umkd_num2, lambda c: c.data.startswith('umkdp1:'))
    nihao.callback_query.register(Get_umkd_tch.button_pressed_umkd_download, lambda c: c.data.startswith('umkds1:'))

    nihao.callback_query.register(Get_jornal_tch.jornal_1, lambda c: c.data.startswith('jornalTch:'))
    nihao.callback_query.register(Get_jornal_tch.jornal_2, lambda c: c.data.startswith('jornalTchk:'))

    nihao.callback_query.register(Get_practika.jornal_1, lambda c: c.data.startswith('attendanceTch1:'))
    nihao.callback_query.register(Get_practika.jornal_2, lambda c: c.data.startswith('attendanceTchk1:'))


    nihao.callback_query.register(Get_attendance.jornal_1, lambda c: c.data.startswith('attendanceTch:'))
    nihao.callback_query.register(Get_attendance.jornal_2, lambda c: c.data.startswith('attendanceTchk:'))


    nihao.message.register(dist_course, StateFilter(FSM.DistCour))
    nihao.message.register(dist_course_for_tchr, StateFilter(FSM.DistCour_thcr))
    nihao.message.register(Get_examus.examus, StateFilter(FSM.Examus))
    nihao.message.register(Get_jornal.jornal, StateFilter(FSM.Jornal))
    nihao.message.register(Get_schedule.schedule, StateFilter(FSM.Schedule))
    nihao.message.register(Get_umkd.umkd, StateFilter(FSM.Umkd))
    nihao.message.register(Get_practics.practics, StateFilter(FSM.Practics))
    nihao.message.register(Get_adviser.Adviser, StateFilter(FSM.Adviser))
    nihao.message.register(Get_transkript.Transkript, StateFilter(FSM.Transkript))
    nihao.message.register(Get_Plan.plan, StateFilter(FSM.Plan))
    nihao.message.register(Get_academcalendar.Calendar, StateFilter(FSM.Calendar))
    nihao.message.register(Get_userplan.Userplan, StateFilter(FSM.Userplan))

    nihao.message.register(Get_jornal_tch.jornal, StateFilter(FSM.Jornaltch))
    nihao.message.register(Get_attendance.jornal, StateFilter(FSM.Attendance))
    nihao.message.register(Get_schld_tch.schld, StateFilter(FSM.Schld))
    nihao.message.register(Get_shchldex.schld, StateFilter(FSM.SchldEX))
    nihao.message.register(Get_umkd_tch.umkd, StateFilter(FSM.Umkdtch))
    nihao.message.register(Get_practika.jornal, StateFilter(FSM.Praktika))
    nihao.message.register(Get_students.std, StateFilter(FSM.Students))

