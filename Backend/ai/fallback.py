from Backend.ai.platforms import create_search_link


def home_recommendation(data):
    budget = float(data.get("budget", 0))
    room = data.get("room", "Living Room")
    style = data.get("style", "Modern")
    people = data.get("people", "2")

    items = []

    if budget >= 1000:
        items.append({
            "name": f"{style} {room} Decor Set",
            "category": "Home Decor",
            "price": round(budget * 0.35, 2),
            "platform": "IKEA",
            "link": create_search_link(
                "IKEA",
                f"{style} {room} decor"
            )
        })

    items.append({
        "name": f"{style} Cushion Set",
        "category": "Soft Furnishing",
        "price": round(budget * 0.10, 2),
        "platform": "Amazon",
        "link": create_search_link(
            "Amazon",
            f"{style} cushion set"
        )
    })

    items.append({
        "name": f"{style} Wall Decoration",
        "category": "Wall Decor",
        "price": round(budget * 0.15, 2),
        "platform": "Flipkart",
        "link": create_search_link(
            "Flipkart",
            f"{style} wall decoration"
        )
    })

    return {
        "planner": "Home",
        "summary": (
            f"Budget-friendly {style} ideas for your "
            f"{room}, suitable for {people} people."
        ),
        "items": items
    }


def party_recommendation(data):
    budget = float(data.get("budget", 0))
    event = data.get("event", "Birthday")
    guests = data.get("guests", "10")
    theme = data.get("theme", "Simple")

    items = [
        {
            "name": f"{theme} {event} Decoration",
            "category": "Decoration",
            "price": round(budget * 0.25, 2),
            "platform": "Amazon",
            "link": create_search_link(
                "Amazon",
                f"{theme} {event} decoration"
            )
        },
        {
            "name": f"{event} Cake",
            "category": "Food",
            "price": round(budget * 0.25, 2),
            "platform": "Swiggy",
            "link": create_search_link(
                "Swiggy",
                f"{event} cake"
            )
        },
        {
            "name": "Party Accessories",
            "category": "Accessories",
            "price": round(budget * 0.10, 2),
            "platform": "Flipkart",
            "link": create_search_link(
                "Flipkart",
                "party accessories"
            )
        }
    ]

    return {
        "planner": "Party",
        "summary": (
            f"A {theme} {event} plan for approximately "
            f"{guests} guests."
        ),
        "items": items
    }


def jewelry_recommendation(data):
    budget = float(data.get("budget", 0))
    occasion = data.get("occasion", "Casual")
    metal = data.get("metal", "Gold")

    items = [
        {
            "name": f"{metal} Earrings",
            "category": "Earrings",
            "price": round(budget * 0.30, 2),
            "platform": "Amazon",
            "link": create_search_link(
                "Amazon",
                f"{metal} earrings {occasion}"
            )
        },
        {
            "name": f"{metal} Necklace",
            "category": "Necklace",
            "price": round(budget * 0.45, 2),
            "platform": "Flipkart",
            "link": create_search_link(
                "Flipkart",
                f"{metal} necklace {occasion}"
            )
        },
        {
            "name": f"{metal} Bracelet",
            "category": "Bracelet",
            "price": round(budget * 0.20, 2),
            "platform": "Amazon",
            "link": create_search_link(
                "Amazon",
                f"{metal} bracelet {occasion}"
            )
        }
    ]

    return {
        "planner": "Jewelry",
        "summary": (
            f"{metal} jewelry suggestions for a "
            f"{occasion} occasion."
        ),
        "items": items
    }