#pragma once

#include <string>

class FuelController {
public:
    explicit FuelController(double fuel_rate);

    double dispenseFuel(double liters);
    void logSession(const std::string& session_id);

private:
    double fuel_rate_;
};
