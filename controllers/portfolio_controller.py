from __future__ import annotations

import os

from flask import Blueprint, render_template

from services.portfolio_service import PortfolioService


portfolio_bp = Blueprint("portfolio", __name__)


@portfolio_bp.route("/")
def home() -> str:
    username = os.getenv("GITHUB_USERNAME", "MiguelAntoniox")
    portfolio = PortfolioService().build_portfolio(username)
    return render_template("index.html", portfolio=portfolio)
