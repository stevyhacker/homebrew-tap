cask "lokalbot" do
  version "0.9.0"
  sha256 "b13b210d820ef3c6d2c3add7cd053a7268524d698d5f8ee1d44d20156628aac8"

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
