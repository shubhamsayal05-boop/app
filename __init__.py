"""
The ODRIV Dashboard Module
===========================

This module provides a main‐function which accepts a uuid string and returns
a WSGI application which can be used by AVL‐DRIVE.
"""

from flask import Flask
from . import app

def main(uuid: str, session) -> Flask:
    """
    Main function called by AVL-DRIVE.
   
    Parameters
    ----------
    uuid : str
        The unique ID which is assigned to the application on dashboard creation.
   
    session: DriveSession
        The avl_drive session (unused by Dash but required by AVL-DRIVE API).
   
    Returns
    -------
    Flask
        The Flask web server (Dash.app.server).
    """
    # app.main returns a Dash instance; its .server is the Flask server used by AVL-DRIVE.
    return app.main(uuid, session).server