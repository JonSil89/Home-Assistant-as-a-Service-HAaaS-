/**
 * HAaaS Device Monitoring Logic - Jonne Silvennoinen 2026
 * Demonstrating TypeScript interfaces for IoT telemetry.
 */

interface DeviceStatus {
    id: string;
    type: 'sensor' | 'actuator';
    batteryLevel: number;
    isOnline: boolean;
    lastSeen: Date;
}

const validateDevice = (device: DeviceStatus): string => {
    console.log(`--- 🔍 Monitoring Device: ${device.id} ---`);
    
    if (device.batteryLevel < 20) {
        return `⚠️ LOW BATTERY: ${device.batteryLevel}% - Maintenance ticket required.`;
    }
    
    if (!device.isOnline) {
        return `🚨 OFFLINE: Device ${device.id} unreachable. Initiating DLCM recovery...`;
    }

    return `✅ OK: Device is operational and compliant.`;
};

// Example usage
const mySensor: DeviceStatus = {
    id: "THERM-001",
    type: "sensor",
    batteryLevel: 15,
    isOnline: true,
    lastSeen: new Date()
};

console.log(validateDevice(mySensor));
