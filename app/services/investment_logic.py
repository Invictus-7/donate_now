from datetime import datetime


def donation_investment(donation, not_closed_projects):
    """Процесс инвестирования в случае, когда есть незакрытые проекты
    и при этом вносится пожертвование."""

    for project in not_closed_projects:

        donation_possible = donation.full_amount - donation.invested_amount

        # Если вложенных денег не хватает даже чтобы закрыть хотя бы один проект
        if project.invested_amount + donation_possible < project.full_amount:
            project.invested_amount = project.invested_amount + donation_possible
            # указываем, что все поступившие деньги были распределены
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True  # закрываем пожертвование
            donation.close_date = datetime.utcnow()

            donation_possible = 0

        # Если вложенных денег хватает как раз для закрытия одного проекта
        if project.invested_amount + donation_possible == project.full_amount:
            project.invested_amount = project.invested_amount + donation_possible
            # указываем, что все поступившие деньги были распределены
            donation.invested_amount = donation.full_amount
            project.fully_invested = True  # закрываем проект
            project.close_date = datetime.utcnow()
            donation.fully_invested = True  # закрываем пожертвование
            donation.close_date = datetime.utcnow()

            donation_possible = 0

        # Если вложенных денег хватило для закрытия проекта и еще осталась сумма сверху
        if project.invested_amount + donation_possible > project.full_amount:
            full_excessive_sum = project.invested_amount + donation_possible
            remaining_money = full_excessive_sum - project.full_amount
            project.invested_amount = project.full_amount
            project.fully_invested = True  # закрываем проект
            project.close_date = datetime.utcnow()
            donation.invested_amount = donation.full_amount - remaining_money
            # вычисляем остаток от пожертвований для запуска инвестирования по новому кругу
            # donation_possible = donation.full_amount - donation.invested_amount

    return donation


def project_input(project, not_closed_donations):
    """Процесс инвестирования в случае, когда есть неистраченные
    пожертвования и при этом открывается новый проект."""

    for donation in not_closed_donations:

        project_money_needed = project.full_amount - project.invested_amount
        donation_possible = donation.full_amount - donation.invested_amount

        # Если есть только одно пожертвование и его не хватает для закрытия проекта
        if project_money_needed > donation_possible:
            project.invested_amount = project.invested_amount + donation_possible
            # указываем, что весь свободный донат был распределен
            donation.invested_amount = donation.invested_amount + donation_possible
            donation.fully_invested = True  # закрываем пожертвование
            donation.close_date = datetime.utcnow()

        # если имеющееся пожертвование как раз закрывает проект "в ноль"
        if project_money_needed == donation_possible:
            project.invested_amount = project.invested_amount + donation_possible
            # указываем, что весь свободный донат был распределен
            donation.invested_amount = donation_possible
            project.fully_invested = True  # закрываем проект
            project.close_date = datetime.utcnow()
            donation.fully_invested = True  # закрываем пожертвование
            donation.close_date = datetime.utcnow()

            project_money_needed = 0

        # если имеющееся пожертвование превышает требуемую сумму проекта
        if project_money_needed < donation_possible:
            remaining_money = donation_possible - project.full_amount
            project.invested_amount = project.full_amount
            project.fully_invested = True  # закрываем проект
            project.close_date = datetime.utcnow()
            donation.invested_amount = donation.full_amount - remaining_money

    return project
