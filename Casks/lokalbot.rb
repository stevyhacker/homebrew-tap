cask "lokalbot" do
  version "0.8.4"
  sha256 "633efa8ae0ccdb9a1c1928fcd878e37ae155952d4df44028f8ba11310e8c4d3a"

  url "https://github.com/stevyhacker/lokalbot/releases/download/v#{version}/LokalBot.dmg"
  name "LokalBot"
  desc "Local LLM workhorse that keeps a private memory of your workday"
  homepage "https://www.lokalbot.com/"

  livecheck do
    url :url
    strategy :github_releases
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "LokalBot.app"

  zap trash: [
    "~/Library/Application Support/me.dotenv.LokalBot",
    "~/Library/Preferences/me.dotenv.LokalBot.plist",
  ]
end
