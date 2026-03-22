def calculate_fees(amount: float):

    gateway_fee = amount * 0.014
    platform_fee = amount * 0.01

    total = amount + gateway_fee + platform_fee

    return {
        "amount": amount,
        "gateway_fee": gateway_fee,
        "platform_fee": platform_fee,
        "total": total
    }
