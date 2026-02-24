-- EcoCleanUp Hub - Database Population Script
-- COMP639 S1 2026
-- PostgreSQL
-- Encoding: ASCII-safe (no special characters, no Maori macrons, no curly quotes)
-- Run AFTER create_database.sql

-- ============================================================
-- USERS: 2 Admins (id 1-2), 5 Leaders (id 3-7), 20 Volunteers (id 8-27)
-- ============================================================
INSERT INTO users (username, password_hash, full_name, email, contact_number, home_address, profile_image, environmental_interests, role, status) VALUES

('admin_sarah',
 'scrypt:32768:8:1$NVq7hp2KmEL9Eowp$abddfeebb53a453b96a5a20f89dbee6300c2e036006c4610a353d6985987b403350a5a91d98cb78bec207b7755b9cec36959904cccb6b5643b3af1dc6f266505',
 'Sarah Mitchell', 'sarah.mitchell@ecocleanup.org', '021-555-0101',
 '14 Parkview Drive, Auckland 1010', NULL,
 'sustainability, conservation, policy', 'admin', 'active'),

('admin_james',
 'scrypt:32768:8:1$sZrNZGV4x52NFA7P$798a5bc05253b1d4c48d540e21b1e1781102a6ebf9cbe8886b4a3d83b8a1ad85e9f473f0ee85f61f2fc95756d88a0e3798fb16dfe86d66f5ad9f4aa4cc036917',
 'James Okafor', 'james.okafor@ecocleanup.org', '021-555-0202',
 '8 Heritage Lane, Wellington 6011', NULL,
 'ocean health, zero waste, education', 'admin', 'active'),

('leader_emma',
 'scrypt:32768:8:1$qEEd652te9LTs3y7$94dca730cc8cee1a829b2cdc1decb3dbdcd3c59d5e341ff25cfc66968ec73157218f92d36b7bc6de85cf6b75f13c9bcb664455b86f6bd9e5c4bb64f6cd4d87f8',
 'Emma Thornton', 'emma.thornton@ecocleanup.org', '021-555-0301',
 '23 Riverbend Road, Christchurch 8011', NULL,
 'beach cleanups, wildlife protection, recycling', 'event_leader', 'active'),

('leader_david',
 'scrypt:32768:8:1$piTRajjc9WN1GYYw$ace25dd3d5de9e24068efcfcb653349322d53d1b6d395f51c5e7909e56b3ed05825250ed048b2fbd90f1ed10af76bf883271fcd164f447a01012187a2523a230',
 'David Kaur', 'david.kaur@ecocleanup.org', '021-555-0302',
 '56 Greenfield Avenue, Hamilton 3204', NULL,
 'tree planting, urban gardening, composting', 'event_leader', 'active'),

('leader_nadia',
 'scrypt:32768:8:1$PnEiKnY6ts5Rg8s1$4b9a1c617f637c339352394a0a461825cd4b763c5d53ba5b634da3e2709cb3a5a2dfa9edf3ca8b47bd3ea3a327f3cec8c5844c23fa94bb66a08873875644b9d9',
 'Nadia Petrova', 'nadia.petrova@ecocleanup.org', '021-555-0303',
 '11 Coastal Crescent, Dunedin 9016', NULL,
 'marine conservation, plastic-free living, awareness', 'event_leader', 'active'),

('leader_tom',
 'scrypt:32768:8:1$OWDsamW2dYXFZ7yx$2b7406c86c3059167763d102b1f22bd584edded06e5d6039caef591f2052cbd1e5ff60440e96f83e348ae38dd4fa4643eb4478c48bba8a049b93ef9c3ce15c8c',
 'Thomas Rivera', 'thomas.rivera@ecocleanup.org', '021-555-0304',
 '88 Fernwood Close, Tauranga 3112', NULL,
 'forest conservation, trail maintenance, ecology', 'event_leader', 'active'),

('leader_priya',
 'scrypt:32768:8:1$qCmhtGZvNNN08Wcl$4b2336374eb71b34f873351135e1393331e5cf65265efc7256af4ffe61bffd17728819b3e7991d231e5ade4840b35c73b1dbd92e28bd192cec99759043cc2d2f',
 'Priya Sharma', 'priya.sharma@ecocleanup.org', '021-555-0305',
 '34 Sunrise Boulevard, Napier 4110', NULL,
 'water conservation, river cleanups, sustainability education', 'event_leader', 'active'),

('v_liam',
 'scrypt:32768:8:1$abRY1Kv2oXXYmvfA$22ae4cbb1cc09d5b3ef637e0e69f8a14aca8c56d2361349149e2eb3fd0fea57db9424f374faa6eecdf1e993b19b9092a636bb005b4358d12a965c06e925687a6',
 'Liam Anderson', 'liam.anderson@email.com', '022-456-0001',
 '3 Maple Street, Auckland 1023', NULL,
 'beach cleanups, recycling', 'volunteer', 'active'),

('v_chloe',
 'scrypt:32768:8:1$zm2gWU3tk3VlPNrm$1ae12ff1a83c7ca5afdf83d528da3417f951a1b530dc09968bbb14e813a3caf96133f9095ee2d4ac9660de48f644fb3170901aff3b5cdba85a5bd513ef201b45',
 'Chloe Bennett', 'chloe.bennett@email.com', '022-456-0002',
 '17 Cedar Lane, Wellington 6021', NULL,
 'tree planting, wildlife', 'volunteer', 'active'),

('v_noah',
 'scrypt:32768:8:1$SMcYGbHhC2WOodQ5$16957d0fc656635269e071492f3db8622583c0d3d3ee4e6f7c97bbe2a8440825548b64222f3498793d653b5b60787951c062890ffa4ec9d9798c65ca71d1bcf9',
 'Noah Williams', 'noah.williams@email.com', '022-456-0003',
 '42 Birch Avenue, Christchurch 8022', NULL,
 'ocean conservation, plastic-free', 'volunteer', 'active'),

('v_ava',
 'scrypt:32768:8:1$7N8f1dO5mwuCalye$5394546b99607488ecfbf80360efdd967339ff6a4b0e693e424c592eca920aaa7ce44442a0b7506619e596850cef3f5ccb48f623ee15cd5ec2b9d217f872cb99',
 'Ava Thompson', 'ava.thompson@email.com', '022-456-0004',
 '9 Rimu Road, Hamilton 3210', NULL,
 'composting, urban gardening', 'volunteer', 'active'),

('v_ethan',
 'scrypt:32768:8:1$4cOpM7rmS7sGG83d$7e734f850c57cc3420ad1135dc6d1ac90d6037c4e93760cb1aaa0049611e7b60abcc917b8b9e2c2ccf97b1879baaacf2a212e11e0334800058718970d64f2533',
 'Ethan Clarke', 'ethan.clarke@email.com', '022-456-0005',
 '55 Pohutukawa Drive, Tauranga 3116', NULL,
 'beach cleanups, recycling', 'volunteer', 'active'),

('v_isabella',
 'scrypt:32768:8:1$tTIz3txeGOFKoiV9$105e9d33986779c72bcc20450b44f056a1910ec6f3703f9115fbf4bb78788457ea0eee2605176fbd7c0864f082dc780f770e18d7bdf553266fea18e889d29ca0',
 'Isabella Martinez', 'isabella.martinez@email.com', '022-456-0006',
 '28 Totara Court, Dunedin 9010', NULL,
 'marine life, water quality', 'volunteer', 'active'),

('v_oliver',
 'scrypt:32768:8:1$jWimK8BG9MEVKPGe$38026c724b326e48547fb6405ce0a4b7d7d38544c962a225c0aa4c81c584956b1ca686f00a40fa917146f62f41f6b45439e11f79bbcb90de56ab99991c231de4',
 'Oliver Chen', 'oliver.chen@email.com', '022-456-0007',
 '71 Kauri Grove, Napier 4112', NULL,
 'zero waste, tree planting', 'volunteer', 'active'),

('v_mia',
 'scrypt:32768:8:1$zyAiya6v7pIQT0yC$64ffb7c2d4e5101b0b29aac87b613525b2f23dd9c1eb033707590fbc38aa2c7cbc2630ed428919c4cdfa3ff95e845d1160f9462f162f0f3ce6e9f59c3ef697f2',
 'Mia Johnson', 'mia.johnson@email.com', '022-456-0008',
 '14 Kowhai Street, Rotorua 3010', NULL,
 'recycling, environmental education', 'volunteer', 'active'),

('v_james_v',
 'scrypt:32768:8:1$OXsSM19ejAMbXQiw$9989ed64da4a1c99c5e1bd19d319570828f273a95030c825bf33b8aa9404aef7f11cf1b91aa695077fb8ba9014a95c03c330a932511370caf86236dc9573566e',
 'James Parker', 'james.parker@email.com', '022-456-0009',
 '6 Nikau Close, Palmerston North 4410', NULL,
 'forest restoration, composting', 'volunteer', 'active'),

('v_sophia',
 'scrypt:32768:8:1$q4eewoqtGwHUCDfU$c52aec503bc38225b0cdeb05cd5f3c69dd3222187b48a047876d5320b135e34d9e76fcd0ca6c486a064e7a6f61ecb9b7b0eebe91fc7db73b6d055b1d80515275',
 'Sophia Lee', 'sophia.lee@email.com', '022-456-0010',
 '33 Manuka Place, Invercargill 9810', NULL,
 'beach cleanups, sea turtle protection', 'volunteer', 'active'),

('v_henry',
 'scrypt:32768:8:1$x73QLqWMG9IUQ1eT$6148ffb76a8c87518d2eaf2d69bd2086a2b28e10b560a9bff8342927f657ace2c5d6eb52efec2e9433981dffd153a695a1d510ee5dc2267091947fca3d9812fa',
 'Henry Wilson', 'henry.wilson@email.com', '022-456-0011',
 '19 Kowhai Road, Nelson 7010', NULL,
 'trail maintenance, conservation', 'volunteer', 'active'),

('v_grace',
 'scrypt:32768:8:1$q84zk3KaLZ4DBtBx$f653a018da0f1fe86c5a5feaee35bde608a05d28f008198309ce3a45a17e56a45b4ee5e65889d6ca5b6608a26a92befcf0088c99d3ac76edc03ea271da123271',
 'Grace Robinson', 'grace.robinson@email.com', '022-456-0012',
 '47 Puka Street, Whangarei 0110', NULL,
 'plastic reduction, ocean health', 'volunteer', 'active'),

('v_william',
 'scrypt:32768:8:1$SNl9wyuo0xQIc5CD$dc44b10c29bb5f4cfcd028adc45b0040dd3cb994c5dd426ebccebab815a4f56a10e0e62ea71fbeeddf951b6fcdc877ec185681c34a21bad530f93e7099b59f65',
 'William Taylor', 'william.taylor@email.com', '022-456-0013',
 '62 Tawa Avenue, Gisborne 4010', NULL,
 'river cleanups, wetland conservation', 'volunteer', 'active'),

('v_amelia',
 'scrypt:32768:8:1$lpe2A4QJlCd93BnJ$95f672f8989a031fb5d66256cd70be7b4d37111e4ec488455138f11acd1f5f59f1c65a00a84e65a130138877c2f3cc716e0db2b6dfe6d449f1321b80d2c6c2d6',
 'Amelia Scott', 'amelia.scott@email.com', '022-456-0014',
 '25 Puriri Close, New Plymouth 4310', NULL,
 'tree planting, sustainable living', 'volunteer', 'active'),

('v_jack',
 'scrypt:32768:8:1$R1gJxsBcUSGJkLgO$53c8743a3bab8a9cf8c1d93e89902a60092f2f124e30ad2d72291294916201f278bb80e357f66f5ec756e653f937184ac6d4b6d5cccf3830047927481a5837ce',
 'Jack Hughes', 'jack.hughes@email.com', '022-456-0015',
 '38 Rimu Street, Timaru 7910', NULL,
 'composting, zero waste', 'volunteer', 'active'),

('v_lily',
 'scrypt:32768:8:1$YyLkVBKF1Mq0Dpf0$a31b7c76327fdfcb21a70d3d595692720727bd285594406b389242232ce8233c4df9adf77f72346176248bbfdbb96b5af488ba851199ffca62577fa78f78d0a5',
 'Lily Adams', 'lily.adams@email.com', '022-456-0016',
 '50 Flaxbush Road, Blenheim 7201', NULL,
 'marine conservation, recycling', 'volunteer', 'active'),

('v_ryan',
 'scrypt:32768:8:1$RAgJtKPhKgqma1wB$5a06b8862cf955978d2c2e2f93faadb8575516581f76e84cbe5c3dbe8c0853516b6e8798480fac3301557ebd00c9b5b582b38faf6978fc267afb025debc4753b',
 'Ryan Brown', 'ryan.brown@email.com', '022-456-0017',
 '12 Cabbage Tree Lane, Hawera 4610', NULL,
 'beach cleanups, awareness campaigns', 'volunteer', 'active'),

('v_emma_v',
 'scrypt:32768:8:1$PORie25xQks5Ourj$2a1fce793c89aa174aaaf5b7d54e62adac8f1a7a1298b3ad01713cba6a023ace99a9a32d249801a2a6482e987cf0a727c3acee498e579c905897c04e2e5e0a25',
 'Emma Walsh', 'emma.walsh@email.com', '022-456-0018',
 '76 Kereru Drive, Whanganui 4500', NULL,
 'forest restoration, bird life', 'volunteer', 'active'),

('v_lucas',
 'scrypt:32768:8:1$9EXuO3xuFTajSL89$83c440c048cd730768ae0e932804e4764dbdbf931fc1391fde3b5c82ffbfb8032e3febe8a489a00551af01d0dea946c6dffb9f2e8b02bb5cd89b99a7e1804093',
 'Lucas Harris', 'lucas.harris@email.com', '022-456-0019',
 '91 Totara Road, Masterton 5810', NULL,
 'river cleanups, composting', 'volunteer', 'active'),

('v_zoe',
 'scrypt:32768:8:1$VO08GNGXCSjOTCGv$046cbc40c925b060bc5b8ff575725ef80cc1f4ddbb1b5062d71c97b388a433f6857ce6b9ac5162a5abec91d8957a1c22c231da74536990cd90a14eef9400b0a7',
 'Zoe Campbell', 'zoe.campbell@email.com', '022-456-0020',
 '5 Punga Place, Levin 5510', NULL,
 'sustainable living, zero waste, recycling', 'volunteer', 'active');


-- ============================================================
-- EVENTS: 25 total
-- COMPLETED (event_id 1-5): referenced by registrations/outcomes/feedback
-- UPCOMING  (event_id 6-25)
-- leader_emma=3, leader_david=4, leader_nadia=5, leader_tom=6, leader_priya=7
-- ============================================================
INSERT INTO events (event_name, event_leader_id, location, event_type, event_date,
                    start_time, end_time, duration, description, supplies, safety_instructions, status) VALUES

-- ---- COMPLETED (1-5) ----
('Piha Beach Cleanup',
 3, 'Piha Beach, Auckland', 'Beach Cleanup', '2026-02-08',
 '08:00', '11:00', 3,
 'A successful cleanup at the iconic Piha Beach. Volunteers collected large amounts of plastic and fishing debris.',
 'Gloves, bags, sunscreen, litter pickers',
 'Strong currents - do not enter water. Stay above the tide line at all times.',
 'completed'),

('Christchurch Avon River Cleanup',
 4, 'Avon River Precinct, Christchurch', 'River Cleanup', '2026-02-15',
 '09:00', '13:00', 4,
 'Volunteers removed litter and weeds from the Avon River banks as part of the Otakaro Avon revival project.',
 'Gloves, weed pullers, bags, gumboots',
 'Slippery banks. No swimming. Closed-toe shoes required.',
 'completed'),

('Island Bay Marine Reserve Cleanup',
 5, 'Island Bay, Wellington', 'Beach Cleanup', '2026-02-22',
 '10:00', '13:00', 3,
 'A focused cleanup around the Island Bay Marine Reserve protecting our precious marine ecosystems.',
 'Gloves, bags, snorkelling gear for shoreline debris',
 'No entry into the marine reserve. Stay on the shoreline.',
 'completed'),

('Hamilton Lake Rubbish Collection',
 6, 'Hamilton Lake, Hamilton', 'Lake Cleanup', '2026-03-01',
 '09:00', '12:00', 3,
 'Volunteers helped clear litter from around Hamilton Lake Domain, making it a better space for wildlife and the community.',
 'Gloves, bags, litter pickers',
 'Stay on paved paths. Report any suspicious items to coordinators.',
 'completed'),

('Tauranga CBD Green Corridor',
 7, 'Tauranga Central City', 'Urban Cleanup', '2026-03-08',
 '08:30', '11:30', 3,
 'Cleaning up the green corridors and reserves in Tauranga city centre to improve urban biodiversity.',
 'Gloves, bags, pruning shears, weed mats',
 'Wear gloves at all times. Watch for traffic near roadways.',
 'completed'),

-- ---- UPCOMING (6-25) ----
('Takapuna Beach Cleanup',
 3, 'Takapuna Beach, Auckland', 'Beach Cleanup', '2026-03-15',
 '08:00', '11:00', 3,
 'Join us for a morning cleanup at Takapuna Beach. We will focus on removing plastic debris and fishing lines.',
 'Gloves, rubbish bags, sunscreen, water bottle',
 'Wear sturdy footwear. Do not touch syringes or sharp objects. Stay above the waterline.',
 'upcoming'),

('Hagley Park Tree Planting',
 4, 'Hagley Park, Christchurch', 'Tree Planting', '2026-03-22',
 '09:00', '13:00', 4,
 'Help restore native biodiversity in Hagley Park by planting native trees and shrubs. All skill levels welcome.',
 'Spades, gardening gloves, native seedlings provided, water',
 'Wear appropriate clothing. Use sunscreen. Watch for uneven ground.',
 'upcoming'),

('Wellington Harbour Litter Blitz',
 5, 'Oriental Parade, Wellington', 'Beach Cleanup', '2026-03-29',
 '09:30', '12:30', 3,
 'Clear plastic waste and litter from the Wellington waterfront. Teams will cover different sections of the harbour.',
 'Rubbish bags, gloves, litter pickers',
 'Be cautious of traffic near roadside areas. Wear hi-vis vests provided.',
 'upcoming'),

('Waikato River Restoration',
 6, 'Ngaruawahia Riverbank, Hamilton', 'River Cleanup', '2026-04-05',
 '08:30', '12:30', 4,
 'Restore the Waikato River banks by removing invasive weeds and collecting litter from the riverside.',
 'Gloves, weed pullers, rubbish bags, gumboots recommended',
 'Slippery conditions near the water. Wear closed-toe footwear. No swimming.',
 'upcoming'),

('Mount Maunganui Dune Restoration',
 7, 'Mount Maunganui Beach, Tauranga', 'Dune Restoration', '2026-04-12',
 '08:00', '12:00', 4,
 'Help stabilise the dunes at the Mount by removing invasive marram grass and planting native spinifex.',
 'Gloves, planting spades, native plants provided',
 'Watch for uneven terrain on dunes. Wear sturdy shoes.',
 'upcoming'),

('Devonport Beach Morning Cleanup',
 3, 'Devonport Beach, Auckland', 'Beach Cleanup', '2026-04-19',
 '07:30', '10:30', 3,
 'Early morning cleanup at Devonport Beach. Bring your friends and family for a great community experience.',
 'Gloves, bags, sunscreen',
 'Stay above the tide line. Children must be accompanied by an adult.',
 'upcoming'),

('Otago Peninsula Bird Habitat Cleanup',
 5, 'Otago Peninsula, Dunedin', 'Habitat Restoration', '2026-04-26',
 '09:00', '14:00', 5,
 'Protect the yellow-eyed penguin habitat by clearing litter and invasive weeds around nesting areas.',
 'Gloves, bags, secateurs for weed removal',
 'Maintain quiet near nesting areas. Do not disturb wildlife. Stay on marked paths.',
 'upcoming'),

('Rotorua Lake Litter Collection',
 6, 'Lake Rotorua Lakefront, Rotorua', 'Lake Cleanup', '2026-05-03',
 '09:00', '12:00', 3,
 'Collect litter around the Rotorua lakefront and nearby reserves to keep the area pristine.',
 'Rubbish bags, gloves, litter pickers',
 'Wear weather-appropriate clothing. Be mindful of geothermal activity in the area.',
 'upcoming'),

('Nelson Tasman Park Cleanup',
 4, 'Tasman District, Nelson', 'Park Cleanup', '2026-05-10',
 '10:00', '14:00', 4,
 'Join us for a comprehensive cleanup of the Nelson-Tasman regional park trails and picnic areas.',
 'Gloves, bags, brooms for trail clearing',
 'Wear appropriate footwear for trails. Carry water. No dogs on this event.',
 'upcoming'),

('Napier Foreshore Cleanup',
 7, 'Marine Parade, Napier', 'Beach Cleanup', '2026-05-17',
 '09:00', '12:00', 3,
 'Keep Napier foreshore beautiful by collecting litter along Marine Parade and the beach.',
 'Gloves, bags, litter pickers',
 'Be aware of traffic. Wear hi-vis vests provided. Slip-on footwear not permitted.',
 'upcoming'),

('Gulf Harbour Beach Cleanup',
 3, 'Gulf Harbour, Whangaparaoa', 'Beach Cleanup', '2026-05-24',
 '08:00', '11:00', 3,
 'Remove marine litter from Gulf Harbour marina area and the surrounding beach.',
 'Gloves, bags, litter pickers, sunscreen',
 'Slippery rocks near the marina. Wear sturdy footwear.',
 'upcoming'),

('Palmerston North River Corridor',
 7, 'Manawatu River, Palmerston North', 'River Cleanup', '2026-05-31',
 '09:00', '13:00', 4,
 'Restore the Manawatu River corridor by removing litter and pest plants from the riverbanks.',
 'Gloves, bags, weed tools, gumboots',
 'Wear gumboots. Be cautious near the river edge. No swimming.',
 'upcoming'),

('Whangarei Town Basin Cleanup',
 4, 'Town Basin, Whangarei', 'Waterway Cleanup', '2026-06-07',
 '10:00', '13:00', 3,
 'Clean up the Town Basin waterway and surrounding park to protect the Hatea River estuary.',
 'Gloves, bags, litter pickers',
 'Wear hi-vis vests provided. Be careful on wet pontoons.',
 'upcoming'),

('New Plymouth Coastal Trail Cleanup',
 5, 'Coastal Walkway, New Plymouth', 'Coastal Cleanup', '2026-06-14',
 '09:00', '12:00', 3,
 'Maintain the beautiful New Plymouth Coastal Walkway by collecting litter from the trail and beach.',
 'Gloves, bags, water bottle',
 'Uneven terrain in places. Wear sturdy shoes. Wet weather gear if needed.',
 'upcoming'),

('Invercargill Waihopai River Cleanup',
 6, 'Waihopai River, Invercargill', 'River Cleanup', '2026-06-21',
 '10:00', '14:00', 4,
 'Restore the Waihopai River environment by removing litter and invasive vegetation.',
 'Gloves, bags, pruning tools, gumboots',
 'Cold conditions expected. Dress in layers. No swimming.',
 'upcoming'),

('Blenheim Wairau River Cleanup',
 7, 'Wairau River, Blenheim', 'River Cleanup', '2026-06-28',
 '09:30', '12:30', 3,
 'Clean up the Wairau River banks and remove plastic waste in the Marlborough region.',
 'Gloves, bags, weed pullers',
 'Slippery banks. Closed-toe footwear required. Watch for river flooding.',
 'upcoming'),

('Coromandel Hahei Beach Cleanup',
 3, 'Hahei Beach, Coromandel', 'Beach Cleanup', '2026-07-05',
 '08:30', '12:30', 4,
 'Protect the pristine Hahei Beach environment from coastal litter and plastic pollution.',
 'Gloves, bags, litter pickers, sunscreen',
 'Remote location. Bring sufficient water. Wear sun protection.',
 'upcoming'),

('Queenstown Wakatipu Lake Cleanup',
 4, 'Lake Wakatipu, Queenstown', 'Lake Cleanup', '2026-07-12',
 '09:00', '13:00', 4,
 'Preserve the stunning Lake Wakatipu shoreline by collecting litter from the Queenstown lakefront.',
 'Gloves, bags, litter pickers, warm clothing',
 'Cold alpine conditions. Dress in warm layers. Wear waterproof footwear.',
 'upcoming'),

('Gisborne Wainui Beach Cleanup',
 5, 'Wainui Beach, Gisborne', 'Beach Cleanup', '2026-07-19',
 '09:00', '12:00', 3,
 'First in NZ to see the sun - keep Wainui Beach pristine! Collect coastal litter and record what we find.',
 'Gloves, bags, data recording sheets, sunscreen',
 'Strong winds possible. Dress for weather. Stay above the tide line.',
 'upcoming'),

('Hawkes Bay Wetland Restoration',
 7, 'Pekapeka Wetland, Hastings', 'Habitat Restoration', '2026-07-26',
 '09:00', '14:00', 5,
 'Help restore the Pekapeka wetland by removing invasive plants and restoring native habitat for birds.',
 'Gloves, gumboots, weed tools, planting spades',
 'Boggy conditions. Wear gumboots. Watch for deep water.',
 'upcoming'),

('Kapiti Coast Shoreline Survey',
 6, 'Kapiti Island, Paraparaumu', 'Coastal Cleanup', '2026-08-02',
 '08:00', '14:00', 6,
 'A full day survey and cleanup of the Kapiti Coast shoreline, recording marine debris data for national research.',
 'Gloves, bags, data collection forms, lunch, water',
 'Full day event. Bring lunch and water. Weather dependent - check the day before.',
 'upcoming');


-- ============================================================
-- EVENT REGISTRATIONS (27 total)
-- Completed events use event_id 1-5
-- Upcoming events use event_id 6-13
-- Volunteer user_ids: v_liam=8, v_chloe=9, v_noah=10, v_ava=11, v_ethan=12,
--   v_isabella=13, v_oliver=14, v_mia=15, v_james_v=16, v_sophia=17,
--   v_henry=18, v_grace=19, v_william=20, v_amelia=21, v_jack=22,
--   v_lily=23, v_ryan=24, v_emma_v=25, v_lucas=26, v_zoe=27
-- ============================================================
INSERT INTO eventregistrations (event_id, volunteer_id, attendance, registered_at) VALUES
-- Completed event 1
(1,  8,  'attended',   '2026-01-25 10:00:00'),
(1,  9,  'attended',   '2026-01-25 10:30:00'),
(1,  10, 'absent',     '2026-01-26 09:00:00'),
(1,  12, 'attended',   '2026-01-26 11:00:00'),
-- Completed event 2
(2,  8,  'attended',   '2026-02-01 09:00:00'),
(2,  11, 'attended',   '2026-02-01 14:00:00'),
(2,  13, 'attended',   '2026-02-02 10:00:00'),
-- Completed event 3
(3,  9,  'attended',   '2026-02-08 09:00:00'),
(3,  14, 'attended',   '2026-02-08 10:00:00'),
(3,  15, 'absent',     '2026-02-09 08:00:00'),
-- Completed event 4
(4,  16, 'attended',   '2026-02-15 12:00:00'),
(4,  17, 'attended',   '2026-02-16 09:00:00'),
(4,  18, 'attended',   '2026-02-16 10:00:00'),
-- Completed event 5
(5,  19, 'attended',   '2026-02-20 11:00:00'),
(5,  20, 'attended',   '2026-02-21 09:00:00'),
-- Upcoming event 6 (Takapuna)
(6,  8,  'registered', '2026-02-20 08:00:00'),
(6,  10, 'registered', '2026-02-21 10:00:00'),
(6,  21, 'registered', '2026-02-22 11:00:00'),
-- Upcoming event 7 (Hagley Park)
(7,  9,  'registered', '2026-02-22 09:00:00'),
(7,  11, 'registered', '2026-02-23 14:00:00'),
-- Upcoming event 8 (Wellington Harbour)
(8,  13, 'registered', '2026-02-23 10:00:00'),
(8,  22, 'registered', '2026-02-24 08:00:00'),
-- Upcoming event 9 (Waikato River)
(9,  23, 'registered', '2026-02-24 09:00:00'),
-- Upcoming event 10 (Mount Maunganui)
(10, 24, 'registered', '2026-02-24 11:00:00'),
-- Upcoming event 11 (Devonport)
(11, 25, 'registered', '2026-02-24 12:00:00'),
-- Upcoming event 12 (Otago Peninsula)
(12, 26, 'registered', '2026-02-24 13:00:00'),
-- Upcoming event 13 (Rotorua Lake)
(13, 27, 'registered', '2026-02-24 14:00:00');


-- ============================================================
-- EVENT OUTCOMES for completed events (event_id 1-5)
-- ============================================================
INSERT INTO eventoutcomes (event_id, num_attendees, bags_collected, recyclables_sorted, other_achievements, recorded_by) VALUES
(1, 3, 18, 7,  'Found and disposed of 2 abandoned fishing nets. Removed 3 car tyres from the dune area.', 3),
(2, 3, 12, 5,  'Removed 50m of invasive crack willow from riverbanks. Planted 30 native flaxes.', 4),
(3, 2, 8,  4,  'Surveyed 400m of shoreline. Documented 3 new pollution hotspots for council follow-up.', 5),
(4, 3, 15, 6,  'Cleared path around the entire lake perimeter. Removed illegal dumping site of old furniture.', 6),
(5, 2, 10, 3,  'Planted 25 native grasses. Cleared invasive weeds from 200 square metres of green corridor.', 7);


-- ============================================================
-- FEEDBACK for completed events (only attended volunteers)
-- ============================================================
INSERT INTO feedback (event_id, volunteer_id, rating, comments, submitted_at) VALUES
(1, 8,  5, 'Fantastic event! Great organization and a real sense of community. Would love to come back.',        '2026-02-09 10:00:00'),
(1, 9,  4, 'Really enjoyed the morning. Would have liked more litter pickers available. Will attend again.',     '2026-02-09 11:00:00'),
(1, 12, 5, 'Amazing experience. Seeing the before and after made it all worthwhile. Emma is a great leader!',   '2026-02-09 14:00:00'),
(2, 8,  4, 'Great river cleanup. The native planting was a bonus. Could use better directional signage.',        '2026-02-16 09:00:00'),
(2, 11, 5, 'One of the best volunteer events I have been to. David knows this area incredibly well.',            '2026-02-16 12:00:00'),
(3, 9,  5, 'Protecting the marine reserve is so important. Nadia kept the team energised the whole time.',      '2026-02-23 10:00:00'),
(3, 14, 4, 'Good event overall. A bit difficult near the rocky shore but safety guidance helped a lot.',         '2026-02-23 15:00:00'),
(4, 16, 5, 'Amazing day at the lake! The illegal dumping site we cleared made a huge difference.',               '2026-03-02 09:00:00'),
(4, 17, 4, 'Tom runs a very efficient operation. Felt like our time was used well. Great teamwork.',             '2026-03-02 11:00:00'),
(5, 19, 5, 'Priya is incredibly knowledgeable about native plants. Learned so much while helping out.',         '2026-03-09 10:00:00');


-- ============================================================
-- NOTIFICATIONS (login popup reminders)
-- Only reference event_id 6-13 (upcoming, verified inserted above)
-- ============================================================
INSERT INTO notifications (user_id, event_id, message, is_read) VALUES
(8,  6,  'Reminder: You are registered for "Takapuna Beach Cleanup" on 15 March 2026 at 08:00. Location: Takapuna Beach, Auckland.',     FALSE),
(10, 6,  'Reminder: You are registered for "Takapuna Beach Cleanup" on 15 March 2026 at 08:00. Location: Takapuna Beach, Auckland.',     FALSE),
(21, 6,  'Reminder: You are registered for "Takapuna Beach Cleanup" on 15 March 2026 at 08:00. Location: Takapuna Beach, Auckland.',     FALSE),
(9,  7,  'Reminder: You are registered for "Hagley Park Tree Planting" on 22 March 2026 at 09:00. Location: Hagley Park, Christchurch.', FALSE),
(11, 7,  'Reminder: You are registered for "Hagley Park Tree Planting" on 22 March 2026 at 09:00. Location: Hagley Park, Christchurch.', FALSE);