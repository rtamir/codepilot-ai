#include "payment/PaymentProcessor.h"

bool PaymentProcessor::authorizeSale(double amount) {
    return amount > 0.0;
}

void PaymentProcessor::captureReceipt(int receipt_id) {
    (void)receipt_id;
}
