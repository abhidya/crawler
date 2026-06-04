from crawler import Crawler


def main():
    data = Crawler.crawl("fixture://home", max_crawl=4)
    assert len(data) == 4
    assert all(item["url"].startswith("fixture://") for item in data)
    assert any(item["url"] == "fixture://api" for item in data)


if __name__ == "__main__":
    main()
