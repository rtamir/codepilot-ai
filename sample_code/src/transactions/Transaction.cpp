#include "transactions/Transaction.h"

Transaction createTransaction(int id, double amount, bool approved) {
    Transaction tx{};
    tx.id = id;
    tx.amount = amount;
    tx.approved = approved;
    return tx;
}
