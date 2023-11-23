from typing import Any,List
import json
import requests
import pandas as pd
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import time

class OmdbAPIConnection(ExperimentalBaseConnection[requests.Session]):
    """Basic st.experimental_connection implementation for IMDB API"""


    def __init__(
        self,
        connection_name: str,
        api_key: str,
        base_url: str = "http://www.omdbapi.com/",
        total_retries: int = 5,
        backoff_factor: float = 0.25,
        status_forcelist: List[int] = None,
        **kwargs,
    ):
        self.base_url = base_url
        self.api_key = api_key

        if status_forcelist is None:
            status_forcelist = [500, 502, 503, 504]
        self.retries = Retry(
            total=total_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )

        super().__init__(connection_name, **kwargs)

    def _connect(
        self, 
        **kwargs: Any
        ) -> requests.Session:
        """
        Connects to the Session

        returns: 
            requests.Session: session
        """
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=self.retries))
        return session

    def cursor(self, **kwargs: Any) -> requests.Session:
        """Returns the session"""
        return self._instance

    def query(
        self, 
        name: str,
        type: str = None,
        year: int = None,
        page: int = 1,
        cache_time: int = 3600, 
        full_information = False,
        **kwargs: Any
        ) -> pd.DataFrame:
        """
        Queries the API .
        
        Parameters:
            query (str): The query string ["s={movie_name}"  Required] 
            {QueryFormat -> "s={movie_name}&type={movie/episode}&y={release_year}&page={page_number}"}
            
            cache_time (int): The time to cache the data in seconds (Default: 3600)

            full_information (bool): If True, returns the full information about the movie
            {Warning: This will make the query slower}

            **kwargs (Any): Any additional arguments to pass to the query

        Returns:
            pd.DataFrame: The results of the query in a dataframe
            for full_information = False -> {Title, Year, imdbID, Type, Poster}
            for full_information = True -> {Title, Year, imdbID, Type, Poster, Rated, Released, Runtime, Genre, Director, Writer, Actors, Plot, Language, Country, Awards,  Metascore, imdbRating, imdbVotes, imdbID, Type, DVD, BoxOffice, Production, Website, totalSeasons}

        Raises:
            Exception: If the API returns an error

        Examples:
            >>> imdb_conn = OmdbAPIConnection("IMDB Connection" , api_key = st.secrets["api_key"])
            >>> df = imdb_conn.query(
            ...     name="Batman",
            ...     type="movie",
            ...     year=2015,
            ...     page=3,
            ...     )
            >>> st.dataframe(df)

        """


        @cache_data(ttl=cache_time)
        def _query(**kwargs: Any) -> pd.DataFrame:
            """Queries the API and returns the results in a dataframe"""
            params = {}
            params["apikey"] = self.api_key
            params["page"] = page
            params["s"] = name
            if type is not None:
                params["type"] = type
            if year is not None:
                params["y"] = year
            if kwargs is not None:
                params.update(kwargs)
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()



            if json.loads(response.text)["Response"] == "False":
                raise Exception(json.loads(response.text)["Error"])
            else:
                result = pd.DataFrame(json.loads(response.text)["Search"])


            if full_information:
                for index, row in result.iterrows():
                    params = {}
                    params["apikey"] = self.api_key
                    params["i"] = row["imdbID"]
                    response = requests.get(self.base_url, params=params)
                    response.raise_for_status()
                    json_response = json.loads(response.text)
                    for key in json_response:
                        if key == "Response" or key =="Ratings":
                            continue
                        else:
                            result.at[index, key] = json_response[key]
            return result

        return _query(**kwargs)
