#include <Wire.h>
#include <AccelStepper.h>
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;
AccelStepper stepper1(AccelStepper::FULL4WIRE, 8, 10, 9, 11); // RA axis
AccelStepper stepper2(AccelStepper::FULL4WIRE, 2, 3, 4, 5);  // DEC axis

float targetYaw = 0.0;   // North direction (0° azimuth)
float targetPitch = 0.0; // 0° altitude

void setup() {
    Serial.begin(9600);
    Wire.begin();
    
    // Initialize MPU-6050
    mpu.initialize();
    if (!mpu.testConnection()) {
        Serial.println("MPU6050 connection failed");
        while (1);
    }

    // Stepper motor settings
    stepper1.setMaxSpeed(1000);
    stepper1.setAcceleration(15);
    stepper2.setMaxSpeed(1000);
    stepper2.setAcceleration(15);
}

void loop() {
    // Read MPU-6050 sensor data
    int16_t ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // Convert raw MPU data to angles (basic estimation)
    float currentYaw = gx / 131.0;
    float currentPitch = ax / 16384.0 * 90.0;

    // Send MPU readings to Python
    Serial.print("MPU:");
    Serial.print(currentYaw);
    Serial.print(",");
    Serial.println(currentPitch);

    // Check if correction is needed
    if (abs(currentYaw - targetYaw) > 0.5 || abs(currentPitch - targetPitch) > 0.5) {
        int moveStepsYaw = (targetYaw - currentYaw) * 10;  // Scale factor for movement
        int moveStepsPitch = (targetPitch - currentPitch) * 10;

        stepper1.moveTo(moveStepsYaw);
        stepper2.moveTo(moveStepsPitch);

        while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
            stepper1.run();
            stepper2.run();
        }
    }
}
