import pytest
from src.app import activities


class TestActivitiesAPI:
    """Test cases for activities API endpoints"""

    def test_get_activities(self, client):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

        # Check that we have some expected activities
        assert "Chess Club" in data
        assert "Programming Class" in data

        # Check structure of activity data
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_has_expected_data(self, client):
        """Test that activities contain expected data"""
        response = client.get("/activities")
        data = response.json()

        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]

    def test_signup_for_activity_success(self, client):
        """Test successful signup for an activity"""
        # Use an activity that exists and an email that's not already signed up
        response = client.post("/activities/Chess%20Club/signup?email=test@example.com")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Signed up test@example.com for Chess Club" in data["message"]

        # Verify the participant was added
        response = client.get("/activities")
        activities_data = response.json()
        assert "test@example.com" in activities_data["Chess Club"]["participants"]

    def test_signup_for_activity_already_signed_up(self, client):
        """Test signup when student is already signed up"""
        # First signup
        client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")

        # Try to signup again
        response = client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student is already signed up" in data["detail"]

    def test_signup_for_nonexistent_activity(self, client):
        """Test signup for activity that doesn't exist"""
        response = client.post("/activities/Nonexistent%20Activity/signup?email=test@example.com")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_from_activity_success(self, client):
        """Test successful unregistration from an activity"""
        # First add a participant
        client.post("/activities/Programming%20Class/signup?email=remove@example.com")

        # Now remove them
        response = client.delete("/activities/Programming%20Class/unregister?email=remove@example.com")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Removed remove@example.com from Programming Class" in data["message"]

        # Verify the participant was removed
        response = client.get("/activities")
        activities_data = response.json()
        assert "remove@example.com" not in activities_data["Programming Class"]["participants"]

    def test_unregister_from_nonexistent_activity(self, client):
        """Test unregistration from activity that doesn't exist"""
        response = client.delete("/activities/Nonexistent%20Activity/unregister?email=test@example.com")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_participant_not_in_activity(self, client):
        """Test unregistration of participant not in the activity"""
        response = client.delete("/activities/Chess%20Club/unregister?email=notparticipating@example.com")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found in this activity" in data["detail"]