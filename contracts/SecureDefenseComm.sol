// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SecureDefenseComm
 * @dev HQ-controlled secure group management for defence personnel
 */
contract SecureDefenseComm {

    address public hqAdmin; // HQ administrator
    uint256 public groupCount; // Counter for group IDs

    struct Group {
        string name;
        address[] members;
        mapping(address => bool) isMember;
        bool exists;
    }

    // Mapping groupID => Group
    mapping(uint256 => Group) private groups;

    // Mapping user => list of group IDs
    mapping(address => uint256[]) private userGroups;

    // Events for logging
    event GroupCreated(uint256 indexed groupId, string name);
    event MemberAdded(uint256 indexed groupId, address member);
    event MemberRemoved(uint256 indexed groupId, address member);

    modifier onlyHQ() {
        require(msg.sender == hqAdmin, "Only HQ Admin can perform this action");
        _;
    }

    modifier groupExists(uint256 _groupId) {
        require(groups[_groupId].exists, "Group does not exist");
        _;
    }

    constructor() {
        hqAdmin = msg.sender; // Deploying account is HQ admin
    }

    /**
     * @dev Create a new secure group
     * @param _name Name of the group
     */
    function createGroup(string memory _name) external onlyHQ returns (uint256) {
        groupCount++;
        Group storage newGroup = groups[groupCount];
        newGroup.name = _name;
        newGroup.exists = true;

        emit GroupCreated(groupCount, _name);
        return groupCount;
    }

    /**
     * @dev Add a member to a group (only HQ can add)
     * @param _groupId ID of the group
     * @param _member Address of the member
     */
    function addMember(uint256 _groupId, address _member) external onlyHQ groupExists(_groupId) {
        Group storage grp = groups[_groupId];
        require(!grp.isMember[_member], "Member already exists");

        grp.members.push(_member);
        grp.isMember[_member] = true;
        userGroups[_member].push(_groupId);

        emit MemberAdded(_groupId, _member);
    }

    /**
     * @dev Remove a member from a group (only HQ can remove)
     * @param _groupId ID of the group
     * @param _member Address of the member
     */
    function removeMember(uint256 _groupId, address _member) external onlyHQ groupExists(_groupId) {
        Group storage grp = groups[_groupId];
        require(grp.isMember[_member], "Member does not exist");

        // Remove from mapping
        grp.isMember[_member] = false;

        // Remove from array (swap & pop for efficiency)
        uint256 len = grp.members.length;
        for (uint256 i = 0; i < len; i++) {
            if (grp.members[i] == _member) {
                grp.members[i] = grp.members[len - 1];
                grp.members.pop();
                break;
            }
        }

        emit MemberRemoved(_groupId, _member);
    }

    /**
     * @dev Get list of members in a group
     * @param _groupId ID of the group
     */
    function getGroupMembers(uint256 _groupId) external view groupExists(_groupId) returns (address[] memory) {
        return groups[_groupId].members;
    }

    /**
     * @dev Check if a user is part of a group
     * @param _groupId ID of the group
     * @param _user Address of the user
     */
    function isMember(uint256 _groupId, address _user) external view groupExists(_groupId) returns (bool) {
        return groups[_groupId].isMember[_user];
    }

    /**
     * @dev Get all groups a user is part of
     * @param _user Address of the user
     */
    function getUserGroups(address _user) external view returns (uint256[] memory) {
        return userGroups[_user];
    }

    /**
     * @dev HQ can transfer admin to another address
     */
    function transferAdmin(address _newAdmin) external onlyHQ {
        require(_newAdmin != address(0), "Invalid address");
        hqAdmin = _newAdmin;
    }
}