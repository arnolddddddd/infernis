"""Tests for lightning pipeline."""

from datetime import date
from unittest.mock import patch

import httpx
import numpy as np

from infernis.pipelines.lightning_pipeline import LightningPipeline


class TestLightningPipeline:
    def test_fetch_returns_correct_shape(self):
        lp = LightningPipeline()
        grid_lats = np.array([50.0, 51.0, 52.0])
        grid_lons = np.array([-120.0, -121.0, -122.0])

        # Mock HTTP to fail — should return zeros gracefully
        with patch.object(lp._client, "get", side_effect=httpx.ConnectError("mocked")):
            result = lp.fetch_lightning_density(grid_lats, grid_lons, date(2025, 7, 15))

        assert result["lightning_24h"].shape == (3,)
        assert result["lightning_72h"].shape == (3,)
        assert np.all(result["lightning_24h"] == 0)
        assert np.all(result["lightning_72h"] == 0)

    def test_fetch_returns_zeros_on_error(self):
        lp = LightningPipeline()
        grid_lats = np.array([50.0, 51.0])
        grid_lons = np.array([-120.0, -121.0])

        with patch.object(lp._client, "get", side_effect=httpx.ConnectError("mocked")):
            result = lp.fetch_lightning_density(grid_lats, grid_lons, date(2000, 1, 1))
        assert result["lightning_24h"].shape == (2,)
        assert result["lightning_72h"].shape == (2,)

    def test_generate_timestamps(self):
        from datetime import datetime, timezone

        lp = LightningPipeline()
        start = datetime(2025, 7, 15, 10, 0, tzinfo=timezone.utc)
        end = datetime(2025, 7, 15, 11, 0, tzinfo=timezone.utc)

        timestamps = lp._generate_timestamps(date(2025, 7, 15), start, end)
        # Should get 6 timestamps: 10:00, 10:10, 10:20, 10:30, 10:40, 10:50
        assert len(timestamps) == 6
        assert timestamps[0] == "20250715T1000Z"
        assert timestamps[-1] == "20250715T1050Z"

    def test_generate_timestamps_empty_window(self):
        from datetime import datetime, timezone

        lp = LightningPipeline()
        # Window doesn't overlap with this day
        start = datetime(2025, 7, 14, 10, 0, tzinfo=timezone.utc)
        end = datetime(2025, 7, 14, 11, 0, tzinfo=timezone.utc)

        timestamps = lp._generate_timestamps(date(2025, 7, 15), start, end)
        assert len(timestamps) == 0
