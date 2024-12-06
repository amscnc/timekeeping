from django.contrib.gis.db.models import Distance
from django.utils.timezone import now
from myapp.models import Venue, Event  # Replace with your actual app name

# User's location (latitude and longitude)
user_location = Point(user_lng, user_lat, srid=4326)

# Radius in miles (e.g., 5 miles)
radius = 5  # Adjust based on your needs

# Query venues within the radius, annotate with distance, and prefetch events
venues_with_events = Venue.objects.filter(
    location__distance_lte=(user_location, D(mi=radius))
).annotate(
    distance=Distance('location', user_location)
).prefetch_related(
    'event_set'  # Adjust if your related name is different
).filter(
    event__date__gte=now()  # Only fetch events that are upcoming
).distinct()


from django.core.serializers import serialize

response_data = {
    "venues": [
        {
            "id": venue.id,
            "name": venue.name,
            "location": {
                "lat": venue.location.y,
                "lng": venue.location.x,
            },
            "distance": venue.distance.mi,  # Convert to miles
            "events": [
                {
                    "id": event.id,
                    "name": event.name,
                    "date": event.date,
                } for event in venue.event_set.all()
            ],
        } for venue in venues_with_events
    ]
}
