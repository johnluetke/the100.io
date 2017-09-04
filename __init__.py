import requests

class _BaseAPI(object):
    """ internal use only """
    # pylint: disable=too-few-public-methods
    def __init__(self, session=None, token=None):
        """ create a base object to make api requests """
        self.token = token
        self.session = session

    def _request(self, api, args):
        """ execute a request to the100.
        Args:
            api (str): the100 API entity
            args (str): specific endpoint of the API entity to query

        Returns:
            dict. JSON response from the100

        Raises:
            requests.error.HTTPError (via requests.raise_for_status())
        """
        url = "https://www.the100.io/api/v1/{}/{}".format(\
            api,\
            args,)

        headers = { "Authorization": "Token {}".format(self.token) }

        print(url)
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json() if response.text else None

class Group(_BaseAPI):
    """ Query the100 for Group information """
    def info(self, group_id):
        """ Return information about the specified group id.

        Args:
            group_id (str): The group's id

        Returns:
            dict.
        """
        return self._request("groups", "{}/".format(group_id))

    def users(self, group_id, page=1):
        """ Return users in the specified group id.

        Args:
            group_id (str): The group's id
            page (int): The page number

        Returns:
            dict.
        """
        return self._request("groups", "{}/users?page={}".format(group_id, page))

    def sessions(self, group_id, page=1):
        """ Return gaming sessions in the specified group id.

        Args:
            group_id (str): The group's id
            page (int): The page number

        Returns:
            dict.
        """
        return self._request("groups", "{}/gaming_sessions?page={}".format(group_id, page))

    def statuses(self, group_id):
        """ Return status from the specified group id.

        Args:
            group_id (str): The group's id

        Returns:
            dict.
        """
        return self._request("groups", "{}/statuses".format(group_id))

class the100io(_BaseAPI):
    # pylint: disable=too-few-public-methods
    def __init__(self, token, default_group=None):
        super(the100io, self).__init__(requests.Session(), token)
        self.group = Group(self.session, self.token)
