from flask import Flask, request, jsonify
import psycopg2
import logging

app = Flask(__name__)
DATABASE = {
    'host': 'test-psql.cov6yxu3ptmd.ap-south-1.rds.amazonaws.com',
    'database': 'testdb',
    'user': 'postgres',
    'password': 'postgres',
}

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


def get_db():
    try:
        return psycopg2.connect(**DATABASE)
    except (psycopg2.OperationalError, psycopg2.Error) as e:
        logging.error(f"Error connecting to the database: {e}")
        raise


@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        username = data['username']
        dob = data['dob']
        email = data['email']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO userschema.users (username, dob, email) VALUES (%s, %s, %s)",
                    (username, dob, email))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({'message': 'User added successfully.'}), 201
    except (psycopg2.OperationalError, psycopg2.Error, KeyError) as e:
        logging.error(f"Error adding user: {e}")
        return jsonify({'error': 'An error occurred while adding the user.'}), 500


@app.route('/api/users/<username>', methods=['PUT'])
def update_user(username):
    try:
        data = request.get_json()
        username = data['username']
        dob = data['dob']
        email = data['email']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE userschema.users SET username=%s, dob=%s, email=%s WHERE username=%s",
                    (username, dob, email, username))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({'message': 'User updated successfully.'}), 200
    except (psycopg2.OperationalError, psycopg2.Error, KeyError) as e:
        logging.error(f"Error updating user: {e}")
        return jsonify({'error': 'An error occurred while updating the user.'}), 500


@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM userschema.users WHERE username=%s", (username,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({'message': 'User deleted successfully.'}), 200
    except (psycopg2.OperationalError, psycopg2.Error) as e:
        logging.error(f"Error deleting user: {e}")
        return jsonify({'error': 'An error occurred while deleting the user.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
