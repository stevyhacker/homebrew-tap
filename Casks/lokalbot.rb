cask "lokalbot" do
  version "0.10.4"
  sha256 "6c67bc9bec32d64204a0171f239973397f635d43af988a4f4a4d7438f5ea789c"

  url "https://github.com/stevyhacker/lokalbot/releases/download/v#{version}/LokalBot.dmg"
  name "LokalBot"
  desc "Find what you said or saw on your Mac"
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
