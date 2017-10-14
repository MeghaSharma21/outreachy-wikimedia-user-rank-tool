import toolforge
import math

from django.http import HttpResponse
from django.shortcuts import render

def userRank(request):
        userData = {}
        resultExists = False
        errorMessage = ''
        isPost = False
        if request.method == 'POST':
                isPost = True
                username = request.POST['username']
                userData = {'username':username}
                try:
                        conn = toolforge.connect('hiwiki')
                        with conn.cursor() as cursor:
                                # finding how many users with the given username exist
                                q1 = cursor.execute('SELECT count(*) FROM user WHERE user_name = %s ',[username])
                                result = cursor.fetchone()
                                if result[0] == 0 :
                                        errorMessage = 'No such user exists!'
                                else:
                                        # finding how many users have greater editcount than that of given username
                                        q2 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount > (SELECT user_editcount FROM user WHERE user_name = %s )',[username])
                                        result = cursor.fetchone()
                                        userRank = result[0]+1
                                        # finding total number of users
                                        q3 = cursor.execute('SELECT count(*) FROM user')
                                        result = cursor.fetchone()
                                        totalNoOfUsers = result[0]
                                        # finding total number of users who have editcount > 0
                                        q4 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount > 0')
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountAtleastOne = result[0]
                                        # finding number of edits made by the user with given username
                                        q5 = cursor.execute('SELECT user_editcount FROM user WHERE user_name = %s',[username])
                                        result = cursor.fetchone()
                                        noOfEditsMade = result[0]
                                        # finding number of users with 0 edits
                                        noOfUsersWithEditCountZero = totalNoOfUsers - noOfUsersWithEditCountAtleastOne
                                        # finding number of users with 1 edit
                                        q6 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount = 1')
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountOne = result[0]
                                        # finding number of users with 2 edits
                                        q7 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount = 2')
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountTwo = result[0]
                                        # finding number of users with 3-5 edits
                                        q8 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount BETWEEN 3 AND 5')
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountBetween3and5 = result[0]
                                        # finding number of users with 6-10 edits
                                        q9 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount BETWEEN 6 AND 10')
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountBetween6and10 = result[0]
                                        # finding number of users with 11-100 edits
                                        q10 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount BETWEEN 11 AND 100')
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountBetween11and100 = result[0]
                                        # finding number of users with 101-1000 edits
                                        q11 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount BETWEEN 101 AND 1000')
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountBetween101and1000 = result[0]
                                        # finding number of users with >1000 edits
                                        q12 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount > 1000')
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountAtleast1001 = result[0]
                                        # calculating percentile of the user
                                        percentile = 100 - (math.ceil(userRank/totalNoOfUsers)*100)
                                        # calculating percentage of users lying in different ranges
                                        percentageOfUsersWith0Edits = 100*round(noOfUsersWithEditCountZero/totalNoOfUsers,2)
                                        percentageOfUsersWith1Edits = 100*round(noOfUsersWithEditCountOne/totalNoOfUsers,2)
                                        percentageOfUsersWith2Edits = 100*round(noOfUsersWithEditCountTwo/totalNoOfUsers,2)
                                        percentageOfUsersWith3to5Edits = 100*round(noOfUsersWithEditCountBetween3and5/totalNoOfUsers,2)
                                        percentageOfUsersWith6to10Edits = 100*round(noOfUsersWithEditCountBetween6and10/totalNoOfUsers,2)
                                        percentageOfUsersWith11to100Edits = 100*round(noOfUsersWithEditCountBetween11and100/totalNoOfUsers,2)
                                        percentageOfUsersWith101to1000Edits = 100*round(noOfUsersWithEditCountBetween101and1000/totalNoOfUsers,2)
                                        percentageOfUsersWithAtleast1001Edits = 100*round(noOfUsersWithEditCountAtleast1001/totalNoOfUsers,2)
                                        # checking which group user with given username belongs to
                                        belongsToGroup = 'group-1';
                                        if noOfEditsMade==0:
                                                belongsToGroup='group-1'
                                        if noOfEditsMade==1:
                                                belongsToGroup='group-2'
                                        if noOfEditsMade==2:
                                                belongsToGroup='group-3'
                                        if noOfEditsMade>=3 and noOfEditsMade<=5:
                                                belongsToGroup='group-4'
                                        if noOfEditsMade>=6 and noOfEditsMade<=10:
                                                belongsToGroup='group-5'
                                        if noOfEditsMade>=11 and noOfEditsMade<=100:
                                                belongsToGroup='group-6'
                                        if noOfEditsMade>=101 and noOfEditsMade<=1000:
                                                belongsToGroup='group-7'
                                        if noOfEditsMade>=1001:
                                                belongsToGroup='group-8'                                                
                                        userData = {
                                                'username': username,
                                                'userRank': userRank,
                                                'percentile': percentile,
                                                'noOfEditsMade': noOfEditsMade,
                                                'totalNoOfUsers': totalNoOfUsers,
                                                'noOfUsersWithEditCountAtleastOne': noOfUsersWithEditCountAtleastOne,
                                                'percentageOfUsersWith0Edits': percentageOfUsersWith0Edits,
                                                'percentageOfUsersWith1Edits': percentageOfUsersWith1Edits,
                                                'percentageOfUsersWith2Edits': percentageOfUsersWith2Edits,
                                                'percentageOfUsersWith3to5Edits': percentageOfUsersWith3to5Edits,
                                                'percentageOfUsersWith6to10Edits': percentageOfUsersWith6to10Edits,
                                                'percentageOfUsersWith11to100Edits': percentageOfUsersWith11to100Edits,
                                                'percentageOfUsersWith101to1000Edits': percentageOfUsersWith101to1000Edits,
                                                'percentageOfUsersWithAtleast1001Edits':percentageOfUsersWithAtleast1001Edits,                          
                                                'belongsToGroup':belongsToGroup
                                        }
                                        resultExists = True
                except Error as e:
                        errorMessage = 'Error fetching results from the Database. If the error persists, contact Megha : meghasharma4910@gmail.com'
                finally:
                        cursor.close()
                        conn.close()
        return render(request, 'user_rank.html', {'isPost':isPost, 'resultExists': resultExists, 'errorMessage': errorMessage, 'userData': userData})
