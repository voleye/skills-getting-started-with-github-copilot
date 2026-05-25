def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert isinstance(payload["Chess Club"]["participants"], list)
    assert isinstance(payload["Chess Club"]["max_participants"], int)


def test_signup_adds_participant_successfully(client):
    email = "new.student@mergington.edu"

    before = client.get("/activities").json()["Chess Club"]["participants"]
    assert email not in before

    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    after = client.get("/activities").json()["Chess Club"]["participants"]
    assert email in after


def test_signup_rejects_duplicate_participant(client):
    email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_rejects_missing_activity(client):
    response = client.post("/activities/Nonexistent%20Club/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant_successfully(client):
    email = "mason@mergington.edu"

    before = client.get("/activities").json()["Debate Team"]["participants"]
    assert email in before

    response = client.post(f"/activities/Debate%20Team/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Debate Team"

    after = client.get("/activities").json()["Debate Team"]["participants"]
    assert email not in after


def test_unregister_rejects_missing_activity(client):
    response = client.post("/activities/Nonexistent%20Club/unregister?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_email_not_signed_up(client):
    response = client.post("/activities/Chess%20Club/unregister?email=not.signed.up@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up"
