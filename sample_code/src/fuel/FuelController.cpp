#include "fuel/FuelController.h"

FuelController::FuelController(double fuel_rate) : fuel_rate_(fuel_rate) {}

double FuelController::dispenseFuel(double liters) {
    return liters * fuel_rate_;
}

void FuelController::logSession(const std::string& session_id) {
    (void)session_id;
}
