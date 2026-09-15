#pragma once

class PaymentProcessor {
public:
    bool authorizeSale(double amount);
    void captureReceipt(int receipt_id);
};
