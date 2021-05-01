from crossbox.models.subscriber import Subscriber


def reset_wods_to_subscrition_amount():
    for sub in Subscriber.objects.all():
        fee = sub.fee
        if fee:
            num_sessions = fee.num_sessions
            sub.wods = num_sessions
            sub.save()


if __name__ == '__main__':
    reset_wods_to_subscrition_amount()
