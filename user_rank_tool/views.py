import toolforge
import math

from django.http import HttpResponse
from django.shortcuts import render

def userRank(request):
        userData = {}
        queryResult = {
                'resultExists': False,
                'errorExists': False,
                'errorMessage': ''
        }
        if request.method == 'POST':
                username = request.POST['username']
                userData = {'username':username}
                try:
                        conn = toolforge.connect('hiwiki')
                        with conn.cursor() as cursor:
                                # finding how many users with the given username exist
                                q1 = cursor.execute('SELECT count(*) FROM user WHERE user_name = %s ',[username])
                                result = cursor.fetchone()
                                if result[0] == 0 :
                                        queryResult['errorExists'] = True
                                        queryResult['errorMessage'] = 'No such user exists!'
                                else:
                                        # finding how many users have greater editcount than that of given username
                                        q2 = cursor.execute('SELECT count(*) FROM user WHERE user_editcount > (SELECT user_editcount FROM user WHERE user_name = %s )',[username])
                                        result = cursor.fetchone()
                                        userRank = result[0]+1
                                        # finding total number of users
                                        q3 = cursor.execute('SELECT count(*) FROM user')
                                        result = cursor.fetchone()
                                        totalNoOfUsers = result[0]
                                        # finding number of edits made by the user with given username
                                        q4 = cursor.execute('SELECT user_editcount FROM user WHERE user_name = %s',[username])
                                        result = cursor.fetchone()
                                        noOfEditsMade = result[0]
                                        # finding number of users in different groups for creating graph
                                        # Definition of 8 groups - list of groups - (lowerlimit, upperlimit) pair - both inclusive
                                        groups = [(0,0),(1,1),(2,2),(3,5),(6,10),(11,100),(101,1000),(1001,2147483648)]
                                        q5 = cursor.execute('SELECT SUM(user_editcount>0), SUM(user_editcount >= %s AND user_editcount <= %s), SUM(user_editcount >= %s AND user_editcount <= %s), SUM(user_editcount >= %s AND user_editcount <= %s),  SUM(user_editcount >= %s AND user_editcount <= %s), SUM(user_editcount >= %s AND user_editcount <= %s), SUM(user_editcount >= %s AND user_editcount <= %s), SUM(user_editcount >= %s AND user_editcount <= %s), SUM(user_editcount >= %s AND user_editcount <= %s) FROM user', [ groups[0][0], groups[0][1], groups[1][0], groups[1][1], groups[2][0], groups[2][1], groups[3][0], groups[3][1], groups[4][0], groups[4][1], groups[5][0], groups[5][1], groups[6][0], groups[6][1], groups[7][0], groups[7][1]])
                                        result = cursor.fetchone()
                                        noOfUsersWithEditCountAtleastOne = result[0]
                                        # noOfUsersInGroup1 is result[1], noOfUsersInGroup2 is result[2], noOfUsersInGroup3 is result[3], noOfUsersInGroup4 is result[4], noOfUsersInGroup5 is result[5], noOfUsersInGroup6 is result[6], noOfUsersInGroup7 is result[7], noOfUsersInGroup8 is result[8]
                                        # calculating percentile of the user
                                        percentile = 100 - 100*round(userRank/totalNoOfUsers,4)
                                        # calculating percentage of users lying in different ranges
                                        # percentageOfUsersInGroup[i] contains percentage of users in ith group 
                                        percentageOfUsersInGroup = [0]*(len(groups)+1)
                                        for i in range(1, len(percentageOfUsersInGroup)):
                                                percentageOfUsersInGroup[i] = round(100*(result[i]/totalNoOfUsers),2)
                                        # checking which group user with given username belongs to
                                        belongsToGroup = 'group-1';
                                        for i in range(len(groups)):
                                                if noOfEditsMade>=groups[i][0] and noOfEditsMade<=groups[i][1]:
                                                        belongsToGroup='group-'+str(i+1)
                                                        break                                   
                                        userData = {
                                                'username': username,
                                                'userRank': userRank,
                                                'percentile': percentile,
                                                'noOfEditsMade': noOfEditsMade,
                                                'totalNoOfUsers': totalNoOfUsers,
                                                'noOfUsersWithEditCountAtleastOne': noOfUsersWithEditCountAtleastOne,
                                                'percentageOfUsersInGroup': percentageOfUsersInGroup,                                                   
                                                'belongsToGroup':belongsToGroup
                                        }
                                        queryResult['resultExists'] = True
                except:
                        queryResult['errorExists'] = True
                        queryResult['errorMessage'] = 'Error fetching results from the Database. If the error persists, contact Megha : meghasharma4910@gmail.com'
                finally:
                        cursor.close()
                        conn.close()
        return render(request, 'user_rank.html', {'result': queryResult, 'userData': userData})