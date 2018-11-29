"""
Expose flask app publicly
"""
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--admin_int', help='Run admin', action='store_true')
    parser.add_argument('--admin_prod', help='Run admin', action='store_true')
    parser.add_argument('--twilio_prod', help='Run admin', action='store_true')

    args = vars(parser.parse_args())
    
    if args['twilio_prod']:
        from server.twilio_app import app
        app.run(host='0.0.0.0', port=8081, debug=False, processes=4)

    elif args['admin_prod']:     
        from server.admin_app import app
        app.run(host='0.0.0.0', port=8080, debug=False, processes=4)

    elif args['admin_int']:     
        from server.admin_app import app
        app.run(host='0.0.0.0', port=5000, debug=True, processes=1)
