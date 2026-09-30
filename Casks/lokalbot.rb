cask "lokalbot" do
  version "0.9.2"
  sha256 "d8bb658b65e91886fa59807fa758e5ae90b38d2e0844dd4498151d083b09de2e"

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
