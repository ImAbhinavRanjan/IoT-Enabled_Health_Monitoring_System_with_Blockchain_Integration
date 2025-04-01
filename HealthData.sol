// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthData {
    struct HealthEntry {
        uint256 timestamp;
        uint256 heartRate;
        uint256 oxygenLevel;
    }

    // Mapping from user ID to their health data
    mapping(uint256 => HealthEntry[]) private userHealthData;

    // Event for new health data added
    event HealthDataAdded(uint256 indexed userId, uint256 heartRate, uint256 oxygenLevel, uint256 timestamp);

    // Function to add health data
    function addHealthData(uint256 userId, uint256 heartRate, uint256 oxygenLevel) public {
        require(heartRate > 0, "Heart rate must be positive");
        require(oxygenLevel > 0, "Oxygen level must be positive");

        userHealthData[userId].push(HealthEntry(block.timestamp, heartRate, oxygenLevel));

        emit HealthDataAdded(userId, heartRate, oxygenLevel, block.timestamp);
    }

    // Function to get all health data for a specific user ID
    function getHealthData(uint256 userId) public view returns (HealthEntry[] memory) {
        return userHealthData[userId];
    }
}
