#!/usr/bin/env python3

import unittest
from server import app
from os import path
from shutil import rmtree
import io


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.client_id = "1000"
        self.client_path = app.config["UPLOADS_PATH"] + "/" + self.client_id
        if path.isdir(self.client_path):
            rmtree(self.client_path)

    def test_normal_flow(self):
        response = self.app.get("/join", headers={"Content-Type": "text/html"})
        self.assertEqual(response.data, b"problems")
        response = self.app.get("/join", 
                headers={"Content-Type": "text/html"}, 
                query_string={"id":self.client_id})
        self.assertGreater(int(response.data), 100000)
        self.assertTrue(path.isdir(self.client_path))
        response = self.app.get("/lastfile", 
                headers={"Content-Type": "text/html"}, 
                query_string={"id":self.client_id})
        self.assertEqual(response.data, b"0.jpg")
        data = { "file": (io.BytesIO(b"aaaaaaa"), "123.jpg") , "id": self.client_id}
        response = self.app.post("/put", data=data, content_type="multipart/form-data")
        self.assertEqual(response.data, b"done")




        




    # curl http://127..0.1:5000/join?id=1
