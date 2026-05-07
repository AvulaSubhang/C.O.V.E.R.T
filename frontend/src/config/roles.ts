/**
 * C.O.V.E.R.T - Role Configuration
 *
 * Maps specific wallet addresses to platform roles.
 * In production, roles are determined by on-chain badge ownership via CovertBadges.
 * This file provides the dev/test fallback using the standard Hardhat/Anvil accounts.
 *
 * Simplified two-role model: user (reporter) and moderator.
 * Moderators can review, finalize, and forward reports to departments.
 *
 * Test accounts (Hardhat / Anvil defaults):
 *   0  0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266  — normal user
 *   1  0x70997970C51812dc3A010C7d01b50e0d17dc79C8  — normal user
 *   3  0x90F79bf6EB2c4f870365E785982E1f101E93b906  — moderator
 *   6  0x976EA74026E726554dB657fA54763abd0C3a0aa9  — moderator
 *   9  0xa0Ee7A142d267C1f36714E4a8F75612F20a79720  — moderator
 */

export type PlatformRole = 'user' | 'moderator';

const MODERATOR_ADDRESSES = new Set([
    '0x90f79bf6eb2c4f870365e785982e1f101e93b906', // Account 3
    '0x976ea74026e726554db657fa54763abd0c3a0aa9', // Account 6
    '0xa0ee7a142d267c1f36714e4a8f75612f20a79720', // Account 9
    '0x67ee12c629784566d5a0548a604b4830e68b5f19', // User Address 2 (Mod)
]);

export function getAddressRole(address: string): PlatformRole {
    const lower = address.toLowerCase();
    if (MODERATOR_ADDRESSES.has(lower)) return 'moderator';
    return 'user';
}

export function isModeratorAddress(address: string): boolean {
    return MODERATOR_ADDRESSES.has(address.toLowerCase());
}

/**
 * Minimum review requirements before a report is considered fully assessed.
 * With the simplified flow, only 1 moderator decision is needed.
 */
export const REVIEW_REQUIREMENTS = {
    minModerators: 1,
} as const;

/** Human-readable role label. */
export const ROLE_LABELS: Record<PlatformRole, string> = {
    user: 'Reporter',
    moderator: 'Protocol Moderator',
};

/** Orange-tinted badge classes per role. */
export const ROLE_BADGE_STYLES: Record<PlatformRole, string> = {
    user: 'bg-neutral-800 text-neutral-300',
    moderator: 'bg-purple-900/40 text-purple-400',
};
