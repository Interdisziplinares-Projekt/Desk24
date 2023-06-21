import flask
import peewee

from warp.db import *
from . import utils
from . import blob_storage

bp = flask.Blueprint('view', __name__)

@bp.context_processor
def headerDataInit():

    headerDataL = []

    zoneCursor = Zone.select(Zone.id, Zone.name) \
                     .join(UserToZoneRoles, on=(Zone.id == UserToZoneRoles.zid)) \
                     .where(UserToZoneRoles.login == flask.g.login) \
                     .order_by(Zone.name)

    for z in zoneCursor:
        headerDataL.append(
            {"text": z['name'], "endpoint": "view.zone", "view_args": {"zid":str(z['id'])} })

    if headerDataL:
        headerDataL.insert(0,{"text": "Bookings", "endpoint": "view.bookings", "view_args": {"report":""} })

    headerDataR = [
        {"text": "Report", "endpoint": "view.bookings", "view_args": {"report": "report"} },
        {"text": "Users", "endpoint": "view.users", "view_args": {} },
        {"text": "Groups", "endpoint": "view.groups", "view_args": {} },
        {"text": "Zones", "endpoint": "view.zones", "view_args": {} }
    ]

    #generate urls and selected
    for hdata in [headerDataL,headerDataR]:

        for h in hdata:

            h['url'] = flask.url_for(h['endpoint'],**h['view_args'])
            a = flask.request.endpoint == h['endpoint']
            b = flask.request.view_args == h['view_args']
            h['active'] = flask.request.endpoint == h['endpoint'] and flask.request.view_args == h['view_args']


    return { "headerDataL": headerDataL,
             "headerDataR": headerDataR,
             'hasLogout': 'auth.logout' in flask.current_app.view_functions
    }

@bp.route("/")
def index():
    current_booking = get_current_booking()
    available_seats = get_available_seats()
    return flask.render_template('index.html',current_booking=current_booking,available_seats=available_seats)

@bp.route("/bookings/<string:report>")
@bp.route("/bookings", defaults={"report": "" })
def bookings(report):

    if report == "report" and not flask.g.isAdmin:
        flask.abort(403)

    return flask.render_template('bookings.html',
        report = (report == "report"),
        maxReportRows = flask.current_app.config['MAX_REPORT_ROWS'])

@bp.route("/zone/<zid>")
def zone(zid):

    zoneRole = UserToZoneRoles.select(UserToZoneRoles.zone_role) \
                              .where( (UserToZoneRoles.zid == zid) & (UserToZoneRoles.login == flask.g.login) ) \
                              .scalar()

    if zoneRole is None:
        flask.abort(403)

    nextWeek = utils.getNextWeek()
    defaultSelectedDates = {
        "slider": [9*3600, 17*3600]
    }

    for d in nextWeek[1:]:
        if not d['isWeekend']:
            defaultSelectedDates['cb'] = [d['timestamp']]
            break

    if zoneRole <= ZONE_ROLE_ADMIN:
        zoneRole = {'isZoneAdmin': True}
    elif zoneRole <= ZONE_ROLE_USER:
        zoneRole = {}
    elif zoneRole <= ZONE_ROLE_VIEWER:
        zoneRole = {'isZoneViewer': True}
    else:
        raise Exception('Undefined role')


    return flask.render_template('zone.html',
        **zoneRole,
        zid = zid,
        nextWeek=nextWeek,
        defaultSelectedDates=defaultSelectedDates)

@bp.route("/zone/image/<zid>")
def zoneImage(zid):

    if not flask.g.isAdmin:

        zoneRole = UserToZoneRoles.select(UserToZoneRoles.zone_role) \
                                .where( (UserToZoneRoles.zid == zid) & (UserToZoneRoles.login == flask.g.login) ) \
                                .scalar()
        if zoneRole is None:
            flask.abort(403)

    blobIdQuery = Zone.select(Zone.iid.alias('id')).where(Zone.id == zid)

    return blob_storage.createBlobResponse(blobIdQuery=blobIdQuery)


@bp.route("/users")
def users():

    if not flask.g.isAdmin:
        flask.abort(403)

    return flask.render_template('users.html')

@bp.route("/groups")
def groups():

    if not flask.g.isAdmin:
        flask.abort(403)

    return flask.render_template('groups.html')

@bp.route("/zones")
def zones():

    if not flask.g.isAdmin:
        flask.abort(403)

    return flask.render_template('zones.html')


@bp.route("/groups/assign/<group_login>")
def groupAssign(group_login):

    if not flask.g.isAdmin:
        flask.abort(403)

    groupName = Users.select(Users.name) \
                     .where( (Users.login == group_login) & (Users.account_type >= ACCOUNT_TYPE_GROUP) ) \
                     .scalar()

    if groupName is None:
        flask.abort(404)

    returnURL = flask.request.args.get('return',flask.url_for('view.groups'))

    return flask.render_template('group_assign.html',
                    groupLogin = group_login,
                    groupName = groupName,
                    returnURL = returnURL)


@bp.route("/zones/assign/<zid>")
def zoneAssign(zid):

    if not flask.g.isAdmin:
        flask.abort(403)

    zoneName = Zone.select(Zone.name) \
                     .where( Zone.id == zid ) \
                     .scalar()

    if zoneName is None:
        flask.abort(404)

    returnURL = flask.request.args.get('return',flask.url_for('view.zones'))

    return flask.render_template('zone_assign.html',
                    zoneName = zoneName,
                    zid = zid,
                    returnURL = returnURL)

@bp.route("/zones/modify/<zid>")
def zoneModify(zid):

    if not flask.g.isAdmin:
        flask.abort(403)

    returnURL = flask.request.args.get('return',flask.url_for('view.zones'))

    return flask.render_template('zone_modify.html',
                    zid = zid,
                    returnURL = returnURL)



import datetime
from peewee import fn, JOIN





def get_current_booking():
    today = datetime.datetime.now().date()
    start_of_day = datetime.datetime.combine(today, datetime.time.min).timestamp()
    end_of_day = datetime.datetime.combine(today, datetime.time.max).timestamp()

    current_booking = Book.select(Seat.name.alias('seat'), Book.fromts, Book.tots) \
                      .join(Seat, on=(Book.sid == Seat.id)) \
                      .where((Book.fromts >= start_of_day) & (Book.fromts <= end_of_day)) \
                      .order_by(Book.fromts) \
                      .first()

    if current_booking:
        seat_name = current_booking.get('seat')
        from_ts = current_booking.get('fromts')
        to_ts = current_booking.get('tots')
        time = f"{utils.formatTimestamp(from_ts)} - {utils.formatTimestamp(to_ts)} Uhr"
        return {"seat": seat_name, "time": time}
    else:
        return None


# Zonen namen anpassen bei änderung
def get_available_seats():
    today = datetime.datetime.now().date()

    seatsEG = (
        Seat
        .select(fn.count(Seat.id))
        .join(Zone, on=(Seat.zid == Zone.id))
        .where(Zone.name == 'Etage 1')
        .scalar(as_tuple=True)[0]
    )
    seatsOG = (
        Seat
        .select(fn.count(Seat.id))
        .join(Zone, on=(Seat.zid == Zone.id))
        .where(Zone.name == 'Etage 2')
        .scalar(as_tuple=True)[0]
    )

    # Gebuchte Plätze für heute abrufen
    bookedEG = (
        Seat
        .select(Seat.id, Book.fromts)
        .join(Book, on=(Seat.id == Book.sid))
        .join(Zone, on=(Seat.zid == Zone.id))
        .where(Zone.name == 'Etage 1')
        .dicts()
    )
    bookedOG = (
        Seat
        .select(Seat.id, Book.fromts)
        .join(Book, on=(Seat.id == Book.sid))
        .join(Zone, on=(Seat.zid == Zone.id))
        .where(Zone.name == 'Etage 2')
        .dicts()
    )

    # Filtern der gebuchten Plätze für heute
    bookedEG_today = sum(1 for booking in bookedEG if datetime.datetime.fromtimestamp(booking['fromts']).date() == today)
    bookedOG_today = sum(1 for booking in bookedOG if datetime.datetime.fromtimestamp(booking['fromts']).date() == today)

    # Verfügbare Sitze berechnen
    availableEG = seatsEG - bookedEG_today
    availableOG = seatsOG - bookedOG_today

    return {
        "EG": availableEG,
        "OG": availableOG
    }

